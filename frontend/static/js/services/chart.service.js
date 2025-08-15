import { getChartContext } from '../utils/dom.utils';

export class ChartService {
  constructor() {
    this.chart = null;
    this.ctx = getChartContext();
  }

  render(sleepData) {
    if (this.chart) {
      this.chart.destroy();
    }

    this.chart = new Chart(this.ctx, {
      type: 'bar',
      data: this._prepareData(sleepData),
      options: this._getOptions()
    });
  }

  _prepareData(sleepData) {
    return {
      labels: sleepData.map(d => new Date(d.start).toLocaleDateString()),
      datasets: [{
        label: 'Sleep Duration (hours)',
        data: sleepData.map(d => d.duration_hours),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    };
  }

  _getOptions() {
    return {
      responsive: true,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: 'Hours' } },
        x: { title: { display: true, text: 'Date' } }
      }
    };
  }
}

export const chartService = new ChartService();

