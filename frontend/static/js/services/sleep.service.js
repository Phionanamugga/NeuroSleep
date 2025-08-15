import { apiService } from './api.service';
import { chartService } from './chart.service';
import { displayStats } from '../utils/dom.utils';
import { showNotification } from '../utils/ui.utils';

export class SleepService {
  static async loadData() {
    try {
      const [sleepData, stats] = await Promise.all([
        apiService.getSleeps(),
        apiService.getStats()
      ]);
      
      displayStats(stats);
      chartService.render(sleepData);
      return sleepData;
    } catch (error) {
      showNotification('Failed to load sleep data', 'error');
      throw error;
    }
  }

  static async addEntry(entry) {
    try {
      await apiService.addSleep(entry);
      await this.loadData();
      showNotification('Sleep entry added!', 'success');
    } catch (error) {
      showNotification('Failed to add entry', 'error');
      throw error;
    }
  }

  static async exportCSV() {
    try {
      const csvData = await apiService.exportCSV();
      this._downloadFile(csvData, 'sleep_export.csv', 'text/csv');
    } catch (error) {
      showNotification('Export failed', 'error');
      throw error;
    }
  }

  static _downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
}

