import React from 'react';

function AdminAbout() {
  return (
    <div className="container mt-4">
      <h2>About QBC App</h2>
      <p><strong>QBC</strong> is a quiz-based competency platform to help students master subjects through structured practice.</p>

      <h4>Key Features</h4>
      <ul>
        <li>Subject & Chapter-wise quizzes</li>
        <li>Cheat sheets for revision</li>
        <li>Question ID search</li>
        <li>Analytics and performance tracking</li>
      </ul>

      <h4>Contact Us</h4>
      <p>Email: <a href="mailto:qbc_admin@fastmail.com">qbc_admin@fastmail.com</a></p>
    </div>
  );
}

export default AdminAbout;
