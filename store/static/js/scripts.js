setTimeout(function() {
    let alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
      // Làm mờ rồi xóa
      alert.classList.remove('show');
      alert.classList.add('fade');
      setTimeout(() => alert.remove(), 500); 
    });
  }, 5000); // sau 5s