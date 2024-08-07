document.addEventListener('DOMContentLoaded', function() {
    function handleResponse(response) {
        if (response.ok) {
            return response.text();
        } else {
            return Promise.reject('Failed to load');
        }
    }

    function updateContent(html) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');

        // Update the body content
        document.body.innerHTML = doc.body.innerHTML;

        // Rebind events
        rebindEvents();

        // Re-execute any scripts
        const scripts = Array.from(doc.querySelectorAll('script'));
        scripts.forEach(oldScript => {
            const newScript = document.createElement('script');
            newScript.textContent = oldScript.textContent;
            oldScript.parentNode.replaceChild(newScript, oldScript);
        });
    }

    function rebindEvents() {
        document.querySelectorAll('a').forEach(function(anchor) {
            anchor.addEventListener('click', function(event) {
                event.preventDefault();
                const url = anchor.href;
                fetch(url, {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(handleResponse)
                .then(updateContent)
                .catch(error => console.error('Error:', error));
            });
        });

        document.querySelectorAll('form').forEach(function(form) {
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                const formData = new FormData(form);
                const url = new URL(form.action);
                const params = new URLSearchParams(formData);

                if (form.method.toUpperCase() === 'GET') {
                    url.search = params.toString();
                    fetch(url.toString(), {
                        method: 'GET',
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    })
                    .then(handleResponse)
                    .then(updateContent)
                    .catch(error => console.error('Error:', error));
                } else {
                    fetch(url.toString(), {
                        method: form.method,
                        body: params,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    })
                    .then(handleResponse)
                    .then(updateContent)
                    .catch(error => console.error('Error:', error));
                }
            });
        });

        // Ensure charts and other components are created only if elements exist
        const ctx = document.getElementById('taskPieChart');

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: [{% for task1 in task_list1 %} '{{task1}}', {% endfor %}],
            datasets: [{
                label: 'Task',
                data: [{% for per in task_per %} '{{per}}', {% endfor %}],
            borderWidth: 1
                }]
            },
            options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
        });
        const ctx1 = document.getElementById('taskGraph');
        new Chart(ctx1, {
            type: 'bar',
            data: {
                labels: [{% for task2 in priority_list %} '{{task2}}', {% endfor %}],
            datasets: [{
                label: 'Task',
                data: [{% for per1 in priority_num %} '{{per1}}', {% endfor %}],
            backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(255, 159, 64, 0.2)',
            'rgba(255, 205, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(201, 203, 207, 0.2)'
        ],
            borderColor: [
            'rgb(255, 99, 132)',
            'rgb(255, 159, 64)',
            'rgb(255, 205, 86)',
            'rgb(75, 192, 192)',
            'rgb(54, 162, 235)',
            'rgb(153, 102, 255)',
            'rgb(201, 203, 207)'
        ],
            borderWidth: 1
                }]
            },
            options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
        });

        document.addEventListener('DOMContentLoaded', function () {
            var calendarEl = document.getElementById('calendar');
            if (calendarEl) {
                var calendar = new FullCalendar.Calendar(calendarEl, {
                    initialView: 'dayGridMonth',
                    events: {
                        url: '/home/api/task_events/',
                        failure: function () {
                            alert('There was an error while fetching events.');
                        }
                    },
                    headerToolbar: {
                        left: 'prev,next today',
                        center: 'title',
                        right: 'dayGridMonth,timeGridWeek,timeGridDay'
                    },
                    eventClick: function (info) {
                        alert('Task: ' + info.event.title);
                    }
                });
                calendar.render();
            } else {
                console.error('Calendar element not found');
            }
        });


        document.addEventListener('DOMContentLoaded', function () {
            var taskModal = document.getElementById('taskModal');
            taskModal.addEventListener('show.bs.modal', function (event) {
                var button = event.relatedTarget;

                // Extract info from data-* attributes
                var title = button.getAttribute('data-title');
                var description = button.getAttribute('data-description');
                var dueDate = button.getAttribute('data-due-date');
                var priority = button.getAttribute('data-priority');
                var category = button.getAttribute('data-category');
                var createdAt = button.getAttribute('data-created-at');
                var editUrl = button.getAttribute('data-edit-url');
                var deleteUrl = button.getAttribute('data-delete-url');

                // Update the modal's content.
                var modalTitle = taskModal.querySelector('#taskTitle');
                var modalDescription = taskModal.querySelector('#taskDescription');
                var modalDueDate = taskModal.querySelector('#taskDueDate');
                var modalPriority = taskModal.querySelector('#taskPriority');
                var modalCategory = taskModal.querySelector('#taskCategory');
                var modalCreatedAt = taskModal.querySelector('#taskCreatedAt');
                var modalEditLink = taskModal.querySelector('#editTaskLink');
                var modalDeleteLink = taskModal.querySelector('#deleteTaskLink');

                modalTitle.textContent = title;
                modalDescription.textContent = description;
                modalDueDate.textContent = dueDate;
                modalPriority.textContent = priority;
                modalCategory.textContent = category;
                modalCreatedAt.textContent = createdAt;
                modalEditLink.href = editUrl;
                modalDeleteLink.href = deleteUrl;
            });
        });
    }

    // Initial binding after ensuring DOM content is loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', rebindEvents);
    } else {
        rebindEvents();
    }
});
