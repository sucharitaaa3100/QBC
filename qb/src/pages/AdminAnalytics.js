import React, { useEffect, useState } from 'react';
import Chart from 'chart.js/auto';

function AdminAnalytics() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/admin/analytics/data')
      .then(res => res.json())
      .then(setData)
      .catch(console.error);
  }, []);

  useEffect(() => {
    if (!data) return;

    new Chart(document.getElementById('subjectPerformanceChart'), {
      type: 'bar',
      data: {
        labels: data.subject_performance.map(s => s.subject),
        datasets: [{ label: 'Avg Score', data: data.subject_performance.map(s => s.avg_score) }]
      }
    });

    new Chart(document.getElementById('qualificationChart'), {
      type: 'pie',
      data: {
        labels: data.qualification_distribution.map(q => q.qualification),
        datasets: [{ data: data.qualification_distribution.map(q => q.count) }]
      }
    });

    new Chart(document.getElementById('performanceChart'), {
      type: 'bar',
      data: {
        labels: data.performance_distribution.map(p => p.score),
        datasets: [{ label: 'Students Count', data: data.performance_distribution.map(p => p.count) }]
      }
    });
  }, [data]);

  if (!data) return <p>Loading Analytics...</p>;

  return (
    <div className="container mt-4">
      <h2>Admin Analytics</h2>

      <div className="row">
        <div className="col-md-4">
          <canvas id="subjectPerformanceChart" />
        </div>
        <div className="col-md-4">
          <canvas id="qualificationChart" />
        </div>
        <div className="col-md-4">
          <canvas id="performanceChart" />
        </div>
      </div>

      <h3 className="mt-5">User Performance</h3>
      <table className="table">
        <thead>
          <tr>
            <th>Name</th><th>Email</th><th>Qualification</th><th>Avg Score</th><th>Quiz Attempts</th>
          </tr>
        </thead>
        <tbody>
          {data.user_performance.map(user => (
            <tr key={user.email}>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.qualification}</td>
              <td>{user.avg_score}</td>
              <td>{user.quiz_attempts}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AdminAnalytics;
