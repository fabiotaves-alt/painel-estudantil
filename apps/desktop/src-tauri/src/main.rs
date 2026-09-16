#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod commands;
mod sidecar;
mod state;

use log::{error, info};
use std::env;
use tauri::Manager;

fn main() {
    env_logger::Builder::from_env(env_logger::Env::default().default_filter_or("info")).init();
    
    // Inicializar SidecarManager e iniciar backend
    let mut sidecar_manager = sidecar::SidecarManager::new();
    
    if let Err(e) = sidecar_manager.start() {
        error!("Falha ao iniciar backend: {}", e);
        eprintln!("Erro crítico: Não foi possível iniciar o backend. Detalhes: {}", e);
        std::process::exit(1);
    }
    
    let backend_url = sidecar_manager.get_url();
    info!("Backend iniciado em {}", backend_url);
    
    let result = tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(state::AppState {
            backend_url: std::sync::Mutex::new(Some(backend_url)),
            backend_port: std::sync::Mutex::new(None),
        })
        .invoke_handler(tauri::generate_handler![
            commands::get_health,
            commands::get_backend_url
        ])
        .run(tauri::generate_context!());

    if let Err(e) = result {
        error!("Erro ao executar aplicação: {}", e);
        std::process::exit(1);
    }
    
    info!("Aplicação encerrada com sucesso");
}
