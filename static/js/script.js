document.addEventListener('DOMContentLoaded', function() {
    fetch('/get-data')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector("#dataTable tbody");

            data.forEach(item => {
                const row = document.createElement("tr");
                
                const nameCell = document.createElement("td");
                nameCell.textContent = item.name;
                row.appendChild(nameCell);

                const ageCell = document.createElement("td");
                ageCell.textContent = item.age;
                row.appendChild(ageCell);

                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('There was an error fetching data:', error);
        });
});
