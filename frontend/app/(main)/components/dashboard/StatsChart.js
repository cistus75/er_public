'use client';

import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Title,
  Ticks,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  Title
);

export default function StatsChart({ stats }) {
  const data = {
    labels: Object.keys(stats),
    datasets: [
      {
        label: '플레이어 통계',
        data: Object.values(stats),
        backgroundColor: 'rgba(230, 230, 230, 1)',
        borderColor: 'rgba(230, 230, 230, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    indexAxis : 'y',
    responsive: true,
    maintainAspectioRatio : false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      x:{
        ticks:{
          color:'#fff'
        }
      },
      y: {
        beginAtZero: true,
        ticks:{
          color:'#fff'
        }
      },
    },
  };

  return <Bar data={data} options={options} />;
}
