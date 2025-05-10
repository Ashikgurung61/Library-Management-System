# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Library Admin Dashboard</title>
#     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    
#     <style>
#         * {
#             margin: 0;
#             padding: 0;
#             box-sizing: border-box;
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#         }

#         body {
#             background: #f5f6fa;
#             display: grid;
#             grid-template-columns: 250px 1fr;
#             min-height: 100vh;
#         }

#         .sidebar {
#             background: #2c3e50;
#             color: white;
#             padding: 20px;
#             position: fixed;
#             height: 100%;
#             width: 250px;
#         }

#         .sidebar-header {
#             padding: 20px;
#             text-align: center;
#             border-bottom: 1px solid #34495e;
#         }

#         .nav-links {
#             margin-top: 30px;
#         }

#         .nav-links a {
#             color: #bdc3c7;
#             text-decoration: none;
#             padding: 15px;
#             display: block;
#             transition: all 0.3s ease;
#         }

#         .nav-links a:hover {
#             background: #34495e;
#             color: white;
#         }

#         .main-content {
#             padding: 30px;
#             margin-left: 250px;
#         }

#         .dashboard-cards {
#             display:grid;
#             grid-template-columns: 1fr 1fr 1fr;
#             gap: 100px;
#             margin-bottom: 30px;
#         }

#         .card {
#             background: white;
#             padding: 20px;
#             border-radius: 10px;
#             box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#             transition: transform 0.3s ease;
#         }

#         .card:hover {
#             transform: translateY(-5px);
#         }

#         .card h3 {
#             color: #4CAF50;
#             margin-bottom: 10px;
#         }

#         .card p {
#             font-size: 1.5rem;
#             font-weight: bold;
#         }

#         .action-section {
#             display: grid;
#             grid-template-columns: 1fr 1fr;
#             gap: 30px;
#             margin-top: 30px;
#         }

#         .form-container {
#             background: white;
#             padding: 25px;
#             border-radius: 10px;
#             box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#         }

#         .form-container h2 {
#             margin-bottom: 20px;
#             color: #2c3e50;
#         }

#         .form-group {
#             margin-bottom: 20px;
#         }

#         .form-group label {
#             display: block;
#             margin-bottom: 8px;
#             color: #666;
#         }

#         .form-group input, .form-group select {
#             width: 100%;
#             padding: 12px;
#             border: 1px solid #ddd;
#             border-radius: 5px;
#             font-size: 16px;
#         }

#         .btn {
#             background: #4CAF50;
#             color: white;
#             padding: 12px 25px;
#             border: none;
#             border-radius: 5px;
#             cursor: pointer;
#             transition: all 0.3s ease;
#         }

#         .btn:hover {
#             background: #45a049;
#             transform: translateY(-2px);
#         }

#         .records-table {
#             background: white;
#             border-radius: 10px;
#             box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#             margin-top: 30px;
#             overflow-x: auto;
#         }

#         table {
#             width: 100%;
#             border-collapse: collapse;
#         }

#         th, td {
#             padding: 15px;
#             text-align: left;
#             border-bottom: 1px solid #eee;
#         }

#         th {
#             background: #f8f9fa;
#             color: #2c3e50;
#         }

#         .status {
#             padding: 5px 10px;
#             border-radius: 20px;
#             font-size: 0.9rem;
#         }

#         .status.issued {
#             background: #ffeeba;
#             color: #856404;
#         }

#         .status.returned {
#             background: #c3e6cb;
#             color: #155724;
#         }

#         .status.overdue {
#             background: #f5c6cb;
#             color: #721c24;
#         }

#         .fine-amount {
#             color: #dc3545;
#             font-weight: bold;
#         }
#     </style>
# </head>
# <body>
#     <div class="sidebar">
#         <div class="sidebar-header">
#             <h2>GurungLib Admin</h2>
#         </div>
#         <div class="nav-links">
#             <a href="#"><i class="fas fa-home"></i> Dashboard</a>
#             <a href="#"><i class="fas fa-book"></i> Manage Books</a>
#             <a href="#"><i class="fas fa-users"></i> Manage Users</a>
#             <a href="#"><i class="fas fa-history"></i> Transaction History</a>
#             <a href="#"><i class="fas fa-dollar-sign"></i> Fines Management</a>
#         </div>
#     </div>

#     <div class="main-content">
#         <div class="dashboard-cards">
#             <div class="card">
#                 <h3>Books Issued</h3>
#                 <p>1,234</p>
#             </div>
#             <div class="card">
#                 <h3>Overdue Books</h3>
#                 <p>56</p>
#             </div>
#             <div class="card">
#                 <h3>Pending Fines</h3>
#                 <p class="fine-amount">$1,230</p>
#             </div>
#         </div>

#         <!-- <div class="action-section">
#             <div class="form-container">
#                 <h2><i class="fas fa-share-square"></i> Issue Book</h2>
#                 <form id="issueForm">
#                     <div class="form-group">
#                         <label>User ID</label>
#                         <input type="text" required>
#                     </div>
#                     <div class="form-group">
#                         <label>Book ID</label>
#                         <input type="text" required>
#                     </div>
#                     <div class="form-group">
#                         <label>Due Date</label>
#                         <input type="date" required>
#                     </div>
#                     <button type="submit" class="btn">Issue Book</button>
#                 </form>
#             </div>

#             <div class="form-container">
#                 <h2><i class="fas fa-undo"></i> Return Book</h2>
#                 <form id="returnForm">
#                     <div class="form-group">
#                         <label>Transaction ID</label>
#                         <input type="text" required>
#                     </div>
#                     <div class="form-group">
#                         <label>Return Date</label>
#                         <input type="date" required>
#                     </div>
#                     <div class="form-group">
#                         <label>Fine Amount</label>
#                         <input type="text" value="$0.00" readonly>
#                     </div>
#                     <button type="submit" class="btn">Process Return</button>
#                 </form>
#             </div>
#         </div>

#         <div class="records-table">
#             <h2 style="padding: 20px 20px 0 20px;">Transaction Records</h2>
#             <div style="padding: 20px;">
#                 <input type="text" placeholder="Search transactions..." style="width: 100%; padding: 10px; margin-bottom: 15px;">
#             </div>
#             <table>
#                 <thead>
#                     <tr>
#                         <th>Transaction ID</th>
#                         <th>User</th>
#                         <th>Book</th>
#                         <th>Issue Date</th>
#                         <th>Due Date</th>
#                         <th>Return Date</th>
#                         <th>Status</th>
#                         <th>Fine</th>
#                     </tr>
#                 </thead>
#                 <tbody>
#                     <tr>
#                         <td>#1234</td>
#                         <td>John Doe</td>
#                         <td>The Great Novel</td>
#                         <td>2023-08-01</td>
#                         <td>2023-08-15</td>
#                         <td>2023-08-16</td>
#                         <td><span class="status overdue">Overdue</span></td>
#                         <td class="fine-amount">$5.00</td>
#                     </tr>
#                 </tbody>
#             </table>
#         </div> -->
#     </div>

#     <script>
#         // Sample fine calculation logic
#         document.getElementById('returnForm').addEventListener('submit', function(e) {
#             e.preventDefault();
#             // Add return processing logic
#             alert('Return processed successfully!');
#         });

#         // Dynamic fine calculation
#         const returnDateInput = document.querySelector('#returnForm input[type="date"]');
#         returnDateInput.addEventListener('change', function() {
#             // Calculate days overdue and fine amount
#             const dueDate = new Date('2023-08-15'); // Get from actual transaction
#             const returnDate = new Date(this.value);
#             const diffTime = Math.max(returnDate - dueDate, 0);
#             const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
#             const fineAmount = diffDays * 2; // $2 per day
            
#             document.querySelector('#returnForm input[type="text"]').value = 
#                 `$${(fineAmount).toFixed(2)}`;
#         });

#         // Search functionality
#         document.querySelector('input[type="text"]').addEventListener('input', function(e) {
#             const searchTerm = e.target.value.toLowerCase();
#             // Add search/filter logic for table
#         });
#     </script>
# </body>
# </html>