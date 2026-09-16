use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct HealthResponse {
    pub status: String,
    pub version: String,
    pub timestamp: String,
}

#[tauri::command]
pub fn get_health() -> Result<HealthResponse, String> {
    Ok(HealthResponse {
        status: "ok".to_string(),
        version: env!("CARGO_PKG_VERSION").to_string(),
        timestamp: chrono::Utc::now().to_rfc3339(),
    })
}

#[tauri::command]
pub fn get_backend_url(state: tauri::State<crate::state::AppState>) -> Result<String, String> {
    state
        .backend_url
        .get()
        .map(|url| url.clone())
        .ok_or_else(|| "Backend URL não disponível".to_string())
}
