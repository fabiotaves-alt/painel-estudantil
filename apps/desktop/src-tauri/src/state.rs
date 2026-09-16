use std::sync::Mutex;

pub struct AppState {
    pub backend_url: Mutex<Option<String>>,
    pub backend_port: Mutex<Option<u16>>,
}

impl Default for AppState {
    fn default() -> Self {
        Self {
            backend_url: Mutex::new(None),
            backend_port: Mutex::new(None),
        }
    }
}
