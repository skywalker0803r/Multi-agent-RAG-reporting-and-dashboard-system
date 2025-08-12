$(document).ready(function() {
    const API_BASE_URL = "http://127.0.0.1:8000/api/v1"; // Replace with your backend URL

    // Generate Report Button Click
    $("#generateReportBtn").click(function() {
        const query = $("#reportQuery").val();
        if (query) {
            $("#reportResult").text("Generating report...").removeClass("text-green-600 text-red-600").addClass("text-gray-600");
            $.ajax({
                url: `${API_BASE_URL}/reports/`,
                type: "POST",
                contentType: "application/json",
                data: JSON.stringify({ query: query }),
                success: function(response) {
                    $("#reportResult").text(response.message + ". Path: " + response.path).removeClass("text-gray-600 text-red-600").addClass("text-green-600");
                },
                error: function(xhr, status, error) {
                    $("#reportResult").text("Error: " + xhr.responseJSON.detail).removeClass("text-gray-600 text-green-600").addClass("text-red-600");
                }
            });
        } else {
            $("#reportResult").text("Please enter a query.").removeClass("text-green-600 text-gray-600").addClass("text-red-600");
        }
    });

    // View Dashboard Button Click
    $("#viewDashboardBtn").click(function() {
        const query = $("#dashboardQuery").val();
        if (query) {
            $("#dashboardResult").text("Fetching dashboard data...").removeClass("text-green-600 text-red-600").addClass("text-gray-600");
            $.ajax({
                url: `${API_BASE_URL}/dashboards/`,
                type: "GET",
                data: { query: query },
                success: function(response) {
                    let dashboardHtml = `<h3>${response.data.title}</h3>`;
                    dashboardHtml += `<p>${response.data.narrative_insights}</p>`;
                    
                    // Basic display for charts (you'd use a charting library here)
                    response.data.charts.forEach(chart => {
                        dashboardHtml += `<div class="mt-4"><h4>${chart.type.charAt(0).toUpperCase() + chart.type.slice(1)} Chart</h4>`;
                        dashboardHtml += `<p>Data: ${chart.data.join(", ")}</p>`;
                        dashboardHtml += `<p>Labels: ${chart.labels.join(", ")}</p></div>`;
                    });

                    $("#dashboardResult").html(dashboardHtml).removeClass("text-gray-600 text-red-600").addClass("text-gray-800");
                },
                error: function(xhr, status, error) {
                    $("#dashboardResult").text("Error: " + xhr.responseJSON.detail).removeClass("text-gray-600 text-green-600").addClass("text-red-600");
                }
            });
        } else {
            $("#dashboardResult").text("Please enter a query.").removeClass("text-green-600 text-gray-600").addClass("text-red-600");
        }
    });
});
