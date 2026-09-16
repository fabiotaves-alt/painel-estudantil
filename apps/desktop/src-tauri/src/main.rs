#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod commands;
mod sidecar;
mod state;

use log::{error, info};
use std::env;
use tauri::Manager;

fn main() {
    env_logger::init();
    
    let result = tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .manage(state::AppState::default())
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
