use log::{error, info, warn};
use std::net::TcpListener;
use std::process::{Child, Command, Stdio};
use std::time::{Duration, Instant};
use std::{env, path::PathBuf};

const MAX_RETRIES: u32 = 30;
const RETRY_DELAY: Duration = Duration::from_millis(500);
const DEFAULT_PORT: u16 = 8000;

pub struct SidecarManager {
    child: Option<Child>,
    port: u16,
}

impl SidecarManager {
    pub fn new() -> Self {
        Self {
            child: None,
            port: DEFAULT_PORT,
        }
    }

    pub fn find_available_port() -> Option<u16> {
        (DEFAULT_PORT..DEFAULT_PORT + 100).find(|port| {
            TcpListener::bind(format!("127.0.0.1:{}", port)).is_ok()
        })
    }

    pub fn start(&mut self) -> Result<(), String> {
        let port = Self::find_available_port().ok_or("Nenhuma porta disponível")?;
        self.port = port;

        let backend_path = self.get_backend_path()?;
        info!("Iniciando backend em: {:?} na porta {}", backend_path, port);

        let child = Command::new(backend_path)
            .arg("--port")
            .arg(port.to_string())
            .arg("--host")
            .arg("127.0.0.1")
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .spawn()
            .map_err(|e| format!("Falha ao iniciar backend: {}", e))?;

        self.child = Some(child);

        if self.wait_for_health(port) {
            info!("Backend iniciado com sucesso na porta {}", port);
            Ok(())
        } else {
            Err("Backend não respondeu ao health check".to_string())
        }
    }

    fn get_backend_path(&self) -> Result<PathBuf, String> {
        #[cfg(debug_assertions)]
        {
            let manifest_dir = env::var("CARGO_MANIFEST_DIR").unwrap_or_else(|_| ".".to_string());
            Ok(PathBuf::from(manifest_dir)
                .join("../../apps/backend/venv/bin/python")
                .canonicalize()
                .map_err(|e| format!("Erro ao resolver caminho: {}", e))?)
        }

        #[cfg(not(debug_assertions))]
        {
            let exe_path = env::current_exe().map_err(|e| e.to_string())?;
            let exe_dir = exe_path.parent().ok_or("Diretório do executável não encontrado")?;
            Ok(exe_dir.join("backend"))
        }
    }

    fn wait_for_health(&self, port: u16) -> bool {
        let client = reqwest::blocking::Client::new();
        let url = format!("http://127.0.0.1:{}/api/v1/health", port);
        let start = Instant::now();

        for attempt in 1..=MAX_RETRIES {
            match client.get(&url).timeout(Duration::from_secs(2)).send() {
                Ok(response) if response.status().is_success() => {
                    info!("Health check bem-sucedido após {} tentativas", attempt);
                    return true;
                }
                Ok(_) => {
                    warn!("Health check retornou status não-ok (tentativa {}/{})", attempt, MAX_RETRIES);
                }
                Err(e) => {
                    warn!("Health check falhou (tentativa {}/{}): {}", attempt, MAX_RETRIES, e);
                }
            }

            if start.elapsed() > Duration::from_secs(15) {
                warn!("Timeout ao aguardar backend");
                break;
            }

            std::thread::sleep(RETRY_DELAY);
        }

        false
    }

    pub fn stop(&mut self) {
        if let Some(mut child) = self.child.take() {
            info!("Encerrando backend...");
            let _ = child.kill();
            let _ = child.wait();
        }
    }

    pub fn get_url(&self) -> String {
        format!("http://127.0.0.1:{}", self.port)
    }
}

impl Drop for SidecarManager {
    fn drop(&mut self) {
        self.stop();
    }
}
