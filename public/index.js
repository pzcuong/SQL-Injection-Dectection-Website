async function Submit() {
    // Get the data from the form id "sql_form"
    const data = document.getElementById("sql_query").value;
    if(data == "") {
        alert("Please enter a query");
        return;
    }
    // Send the data to the server
    const response = await fetch("/check-sql", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ "SQL_Query": data })
    });
    // Get the response from the server
    const result = await response.json();
    alert(result.result);
}