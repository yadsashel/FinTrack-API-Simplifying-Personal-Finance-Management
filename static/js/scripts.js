// Update button functionality
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('updateButton').addEventListener('click', async (event) => {
      event.preventDefault();

      const updatedData = {
          full_name: document.getElementById('full_name').value,
          email: document.getElementById('email').value,
          password: document.getElementById('password').value,
          confirm_password: document.getElementById('confirm_password').value,
          phone: document.getElementById('phone').value,
          address: document.getElementById('address').value,
      };

      try {
          const response = await fetch('/profile', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify(updatedData),
          });

          const result = await response.json();
          if (response.ok) {
              // Redirect to the profile page to refresh and show flash messages
              window.location.href = result.redirect;
          } else {
              alert('An error occurred. Check the flash messages for details.');
          }
      } catch (error) {
          console.error('Error handling profile:', error);
          alert('Something went wrong, please try again.');
      }
  });

  // Hide flash messages
  setTimeout(() => {
      document.querySelectorAll('.alert').forEach(alert => {
          alert.style.opacity = '0';
          setTimeout(() => alert.remove(), 500);
      });
  }, 5000);
});

// Original Chart Configurations
document.addEventListener("DOMContentLoaded", () => {
  const categoryChartCanvas = document.getElementById('categoryChart').getContext('2d');
  const trendsChartCanvas = document.getElementById('trendsChart').getContext('2d');

  // Data for "Expenses by Category"
  const categoryData = {
      labels: ['Rent', 'Gym', 'Groceries', 'Utilities'], // Example categories
      datasets: [
          {
              label: 'Expenses by Category',
              data: [500, 200, 150, 300], // Example data
              backgroundColor: ['#f87171', '#3b82f6', '#10b981', '#fbbf24'], // Colors for each bar
              borderWidth: 1,
          },
      ],
  };

  // Data for "Spending Trends"
  const trendsData = {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May'], // Example months
      datasets: [
          {
              label: 'Spending Trends',
              data: [800, 600, 700, 900, 1000], // Example data
              backgroundColor: '#3b82f6',
              borderColor: '#2563eb',
              borderWidth: 2,
              fill: true,
          },
      ],
  };

  // Configuration for "Expenses by Category" chart
  const categoryChartConfig = {
      type: 'bar',
      data: categoryData,
      options: {
          responsive: true,
          maintainAspectRatio: false, // Allows chart to fill the container
          plugins: {
              legend: {
                  display: true,
                  position: 'top',
              },
              tooltip: {
                  enabled: true,
              },
          },
          scales: {
              x: {
                  title: {
                      display: true,
                      text: 'Categories',
                  },
              },
              y: {
                  title: {
                      display: true,
                      text: 'Amount',
                  },
                  beginAtZero: true,
              },
          },
      },
  };

  // Configuration for "Spending Trends" chart
  const trendsChartConfig = {
      type: 'line',
      data: trendsData,
      options: {
          responsive: true,
          maintainAspectRatio: false, // Allows chart to fill the container
          plugins: {
              legend: {
                  display: true,
                  position: 'top',
              },
              tooltip: {
                  enabled: true,
              },
          },
          scales: {
              x: {
                  title: {
                      display: true,
                      text: 'Months',
                  },
              },
              y: {
                  title: {
                      display: true,
                      text: 'Amount',
                  },
                  beginAtZero: true,
              },
          },
      },
  };

  // Initialize charts
  new Chart(categoryChartCanvas, categoryChartConfig);
  new Chart(trendsChartCanvas, trendsChartConfig);
});

// Handling editing and deleting buttons for the viewtransaction page
document.addEventListener("DOMContentLoaded", () => {
  const editButtons = document.querySelectorAll(".edit-btn");
  const deleteButtons = document.querySelectorAll(".delete-btn");

  // Handle Edit
  editButtons.forEach((button) => {
      button.addEventListener("click", async (e) => {
          const transactionId = e.target.dataset.id;

          // Collect new data via alert prompts
          const newDate = prompt("Enter new date (YYYY-MM-DD):");
          const newType = prompt("Enter new type (income/expense):");
          const newCategory = prompt("Enter new category:");
          const newAmount = prompt("Enter new amount:");

          // Validate input
          if (!newDate || !newType || !newCategory || !newAmount) {
              alert("All fields are required!");
              return;
          }

          // Send the PUT request to update the transaction
          try {
              const response = await fetch(`/edit-transaction/${transactionId}`, {
                  method: "PUT",
                  headers: {
                      "Content-Type": "application/json",
                  },
                  body: JSON.stringify({
                      date: newDate,
                      type: newType,
                      category: newCategory,
                      amount: newAmount,
                  }),
              });

              const data = await response.json();

              if (data.success) {
                  alert(data.message);
                  location.reload(); // Refresh the page to reflect changes
              } else {
                  alert("Failed to edit transaction.");
              }
          } catch (error) {
              console.error("Error:", error);
              alert("An error occurred while editing the transaction.");
          }
      });
  });

  // Handle Delete
  deleteButtons.forEach((button) => {
      button.addEventListener("click", async (e) => {
          const transactionId = e.target.dataset.id;

          // Confirm delete action
          const confirmed = confirm("Are you sure you want to delete this transaction?");
          if (!confirmed) return;

          // Send the DELETE request to delete the transaction
          try {
              const response = await fetch(`/delete-transaction/${transactionId}`, {
                  method: "DELETE",
              });

              const data = await response.json();

              if (data.success) {
                  alert(data.message);
                  location.reload(); // Refresh the page to reflect changes
              } else {
                  alert("Failed to delete transaction.");
              }
          } catch (error) {
              console.error("Error:", error);
              alert("An error occurred while deleting the transaction.");
          }
      });
  });
})


// Handling the charts
document.addEventListener("DOMContentLoaded", () => {
    const getData = (selector, attribute) => {
      const element = document.querySelector(selector);
      try {
        const data = element.dataset[attribute];
        return JSON.parse(data || "[]"); // Default to empty array if data is undefined
      } catch (error) {
        console.error(`Error parsing data-${attribute}:`, error);
        return [];
      }
    };
  
    // Fetch data from the canvas elements
    const categoryLabels = getData("#category-chart", "labels");
    const categoryValues = getData("#category-chart", "values");
    const trendDates = getData("#trend-chart", "dates");
    const trendAmounts = getData("#trend-chart", "amounts");
  
    if (!categoryLabels.length || !categoryValues.length) {
      console.warn("Category data is missing or empty.");
    }
    if (!trendDates.length || !trendAmounts.length) {
      console.warn("Trend data is missing or empty.");
    }
  
    // Expenses by Category Chart
    new Chart(document.getElementById("category-chart"), {
      type: "bar",
      data: {
        labels: categoryLabels,
        datasets: [
          {
            label: "Expenses by Category",
            data: categoryValues,
            backgroundColor: categoryLabels.map((_, i) =>
              `hsl(${(i * 40) % 360}, 70%, 60%)`
            ),
            borderColor: "#fff",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          x: { title: { display: true, text: "Categories" } },
          y: { title: { display: true, text: "Amount ($)" } },
        },
      },
    });
  
    // Spending Trends Chart
    new Chart(document.getElementById("trend-chart"), {
      type: "line",
      data: {
        labels: trendDates,
        datasets: [
          {
            label: "Spending Trends",
            data: trendAmounts,
            borderColor: "#3b82f6",
            backgroundColor: "rgba(59, 130, 246, 0.2)",
            fill: true,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          x: { title: { display: true, text: "Date" } },
          y: { title: { display: true, text: "Amount ($)" } },
        },
      },
    });
  
    // Initialize Charts
    const categoryChartCanvas = document.getElementById("categoryChart").getContext("2d");
    const trendsChartCanvas = document.getElementById("trendsChart").getContext("2d");
  
    const categoryData = {
      labels: ["Rent", "Gym", "Groceries", "Utilities"],
      datasets: [
        {
          label: "Expenses by Category",
          data: [500, 200, 150, 300],
          backgroundColor: ["#f87171", "#3b82f6", "#10b981", "#fbbf24"],
          borderWidth: 1,
        },
      ],
    };
  
    const categoryChartConfig = {
      type: "bar",
      data: categoryData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { title: { display: true, text: "Categories" } },
          y: { title: { display: true, text: "Amount" }, beginAtZero: true },
        },
      },
    };
  
    const trendsData = {
      labels: ["Jan", "Feb", "Mar", "Apr", "May"],
      datasets: [
        {
          label: "Spending Trends",
          data: [800, 600, 700, 900, 1000],
          borderColor: "#2563eb",
          backgroundColor: "#3b82f6",
          fill: true,
        },
      ],
    };
  
    const trendsChartConfig = {
      type: "line",
      data: trendsData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { title: { display: true, text: "Months" } },
          y: { title: { display: true, text: "Amount" }, beginAtZero: true },
        },
      },
    };
  
    new Chart(categoryChartCanvas, categoryChartConfig);
    new Chart(trendsChartCanvas, trendsChartConfig);
  });  
