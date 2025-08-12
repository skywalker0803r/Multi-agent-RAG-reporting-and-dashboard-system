$(document).ready(function() {
    const API_BASE_URL = "http://127.0.0.1:8001/api/v1"; // Updated to 8001

    // Generate Report Button Click
    $("#generateReportBtn").click(function() {
        const query = $("#reportQuery").val();
        if (query) {
            $("#reportResult").text("正在生成報告...").removeClass("text-green-600 text-red-600").addClass("text-gray-600");
            $.ajax({
                url: `${API_BASE_URL}/reports/`,
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ query: query }),
                success: function(response) {
                    const reportContent = response.content;
                    $("#reportResult").html(`<pre class="whitespace-pre-wrap">${reportContent}</pre>`).removeClass("text-gray-600 text-red-600").addClass("text-green-600");
                },
                error: function(xhr, status, error) {
                    // Try to parse JSON, fallback to statusText or generic message
                    let errorMessage = "An unknown error occurred.";
                    if (xhr.responseJSON && xhr.responseJSON.detail) {
                        errorMessage = xhr.responseJSON.detail;
                    } else if (xhr.responseText) {
                        errorMessage = xhr.responseText;
                    } else if (xhr.statusText) {
                        errorMessage = xhr.statusText;
                    }
                    $("#reportResult").text("錯誤: " + errorMessage).removeClass("text-gray-600 text-green-600").addClass("text-red-600");
                }
            });
        } else {
            $("#reportResult").text("請輸入查詢內容。").removeClass("text-green-600 text-gray-600").addClass("text-red-600");
        }
    });

    // View Dashboard Button Click
    $("#viewDashboardBtn").click(function() {
        const query = $("#dashboardQuery").val();
        if (query) {
            $("#dashboardResult").text("正在獲取儀表板數據...").removeClass("text-green-600 text-red-600").addClass("text-gray-600");
            $.ajax({
                url: `${API_BASE_URL}/dashboards/`,
                type: "GET",
                data: { query: query },
                success: function(response) {
                    let dashboardHtml = `<h3 class="text-xl font-semibold mb-2">${response.data.title}</h3>`;
                    dashboardHtml += `<p class="mb-4">${response.data.narrative_insights}</p>`;
                    
                    // Render charts
                    response.data.charts.forEach((chart, index) => {
                        const canvasId = `chartCanvas${index}`;
                        dashboardHtml += `<div class="mb-6"><canvas id="${canvasId}"></canvas></div>`;
                    });

                    $("#dashboardResult").html(dashboardHtml).removeClass("text-gray-600 text-red-600").addClass("text-gray-800");

                    // Initialize Chart.js after canvas elements are in DOM
                    response.data.charts.forEach((chart, index) => {
                        const canvasId = `chartCanvas${index}`;
                        const ctx = document.getElementById(canvasId).getContext('2d');
                        new Chart(ctx, {
                            type: chart.type,
                            data: {
                                labels: chart.labels,
                                datasets: [{
                                    label: chart.type.charAt(0).toUpperCase() + chart.type.slice(1) + ' Data',
                                    data: chart.data,
                                    backgroundColor: chart.type === 'bar' ? 'rgba(75, 192, 192, 0.6)' : 'rgba(153, 102, 255, 0.6)',
                                    borderColor: chart.type === 'bar' ? 'rgba(75, 192, 192, 1)' : 'rgba(153, 102, 255, 1)',
                                    borderWidth: 1
                                }]
                            },
                            options: {
                                responsive: true,
                                scales: {
                                    y: {
                                        beginAtZero: true
                                    }
                                }
                            }
                        });
                    });

                },
                error: function(xhr, status, error) {
                    // Try to parse JSON, fallback to statusText or generic message
                    let errorMessage = "An unknown error occurred.";
                    if (xhr.responseJSON && xhr.responseJSON.detail) {
                        errorMessage = xhr.responseJSON.detail;
                    } else if (xhr.responseText) {
                        errorMessage = xhr.responseText;
                    } else if (xhr.statusText) {
                        errorMessage = xhr.statusText;
                    }
                    $("#dashboardResult").text("錯誤: " + errorMessage).removeClass("text-gray-600 text-green-600").addClass("text-red-600");
                }
            });
        } else {
            $("#dashboardResult").text("請輸入查詢內容。").removeClass("text-green-600 text-gray-600").addClass("text-red-600");
        }
    });
});
