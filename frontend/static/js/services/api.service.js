class ApiService {
  constructor() {
    this.baseUrl = '/api';
    this.token = localStorage.getItem('sleep_tracker_token') || null;
  }

  async _fetch(method, endpoint, data = null) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...(this.token && { 'Authorization': `Bearer ${this.token}` })
    };

    const config = {
      method,
      headers,
      ...(data && { body: JSON.stringify(data) })
    };

    const response = await fetch(url, config);
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(error || 'Request failed');
    }

    return response.json();
  }

  setToken(token) {
    this.token = token;
    token ? localStorage.setItem('sleep_tracker_token', token) 
          : localStorage.removeItem('sleep_tracker_token');
  }

  // Auth endpoints
  register(user) { return this._fetch('POST', '/auth/register', user); }
  login(credentials) { return this._fetch('POST', '/auth/login', credentials); }

  // Sleep endpoints
  getSleeps() { return this._fetch('GET', '/sleeps'); }
  addSleep(entry) { return this._fetch('POST', '/sleeps', entry); }
  getStats() { return this._fetch('GET', '/sleeps/stats'); }
  exportCSV() { return this._fetch('GET', '/export/csv'); }
}

export const apiService = new ApiService();

