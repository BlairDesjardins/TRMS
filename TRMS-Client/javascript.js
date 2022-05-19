async function getRequestsForEmployee(eId) {
    const requestHttpResponse = await fetch(`http://localhost:5000/employees/${eId}/requests`);
    const requests = await requestHttpResponse.json();

    createRequestsTable(requests, false);
}

async function getRequestsForAdmin(eId) {
    const requestHttpResponse = await fetch(`http://localhost:5000/employees/${eId}/requests?admin=true`);
    const requests = await requestHttpResponse.json();

    createRequestsTable(requests, true);
}

let selectedRequest;

async function createRequestsTable(requests, admin) {
    const eventHttpResponse = await fetch(`http://localhost:5000/events`);
    const events = await eventHttpResponse.json();
    
    const formatsHttpResponse = await fetch(`http://localhost:5000/formats`);
    const formats = await formatsHttpResponse.json();

    for (let request of requests) {
        const tbl = document.createElement('table');
        
        const head = tbl.createTHead();
        const headRow = head.insertRow();

        const approvalHead = headRow.insertCell();
        approvalHead.innerHTML = "Approval Status";
        
        const costHead = headRow.insertCell();
        costHead.innerHTML = "Cost";
        
        const amountHead = headRow.insertCell();
        amountHead.innerHTML = "Reimbursement Amount";
        
        const descHead = headRow.insertCell();
        descHead.innerHTML = "Description";
        
        const dateTimeHead = headRow.insertCell();
        dateTimeHead.innerHTML = "Date & Time";

        const locationHead = headRow.insertCell();
        locationHead.innerHTML = "Location";

        const presentationHead = headRow.insertCell();
        presentationHead.innerHTML = "Presentation Required?";

        const gradeHead = headRow.insertCell();
        gradeHead.innerHTML = "Passing Grade";

        const body = tbl.createTBody();
        const tr = body.insertRow();

        let approvalCell = tr.insertCell();
        approvalCell.innerHTML = approvalCodeToWords(request.approvalStatus);

        let costCell = tr.insertCell();
        costCell.innerHTML = request.cost;

        let amountCell = tr.insertCell();
        amountCell.innerHTML = request.cost * events[request.eventTypeId - 1].reimbursementCoverage;
        
        let descCell = tr.insertCell();
        descCell.innerHTML = request.desc;
        
        let dateTimeCell = tr.insertCell();
        dateTimeCell.innerHTML = unix_timestamp_to_datetime(request.datetime);
        
        let locationCell = tr.insertCell();
        locationCell.innerHTML = request.location;

        let presentationCell = tr.insertCell();
        presentationCell.innerHTML = formats[request.gradingId - 1].presentationRequired;
        
        let gradeCell = tr.insertCell();
        gradeCell.innerHTML = formats[request.gradingId - 1].passingGrade;

        if (admin) {
            let aprCell = tr.insertCell();
            let aprBtn = document.createElement('button');
            let aprText = document.createTextNode("Approve");
            aprBtn.addEventListener("click", await approve(request));
            aprBtn.appendChild(aprText);
            aprCell.appendChild(aprBtn);
            
            let rejCell = tr.insertCell();
            let rejBtn = document.createElement('button');
            let rejText = document.createTextNode("Reject");
            rejBtn.addEventListener("click", reject(request));
            rejBtn.appendChild(rejText);
            rejCell.appendChild(rejBtn);
        } else {
            let docCell = tr.insertCell();
            let b = document.createElement('button');
            let t = document.createTextNode("Add Document");
            b.addEventListener("click", addDocument(request));
            b.appendChild(t);
            docCell.appendChild(b);
        }

        document.getElementById("requests").appendChild(tbl)

        await fetch(`http://localhost:5000/requests/${request.rId}/documents`)
            .then(response => {
                if (response.ok) {
                    return response.json()
                } else if(response.status === 404) {
                    return Promise.reject('error 404')
                } else {
                    return Promise.reject('some other error: ' + response.status)
                }
            })
            .then(docs => createDocumentsTable(docs))
            .catch(error => console.log('error is', error));
    }
}

function createDocumentsTable(docs) {
    for (let doc of docs) {
        const tbl = document.createElement('table');
        tbl.style = "margin-left: 50px"
        
        const head = tbl.createTHead();
        const headRow = head.insertRow();
        
        const descHead = headRow.insertCell();
        descHead.innerHTML = "Desciption";
        
        const gradeHead = headRow.insertCell();
        gradeHead.innerHTML = "Grade";
        
        const body = tbl.createTBody();
        const tr = body.insertRow();
        
        let descCell = tr.insertCell();
        descCell.innerHTML = doc.desc;

        let gradeCell = tr.insertCell();
        gradeCell.innerHTML = doc.grade;
        
        document.getElementById("requests").appendChild(tbl)
    }
}

function unix_timestamp_to_datetime(timestamp) {
    let d = new Date(timestamp * 1000);
    
    const date = d.toISOString().split('T')[0];
    const time = d.toTimeString().split(' ')[0];
    return `${date} ${time}`
}

function addDocument(request) {
    return function() {
        let modal = document.getElementById("myModal");
        modal.style.display = "block";
        
        let span = document.getElementsByClassName("close")[0];
        span.onclick = function() {
            modal.style.display = "none";
        }

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

        let btn = document.getElementById("submitDocBtn");
        btn.onclick = function() {
            submitDocument(request);
        }
    }
}

async function approve(request) {
    return async function() {
        const httpResponse = await fetch(`http://localhost:5000/requests/${request.rId}`, {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "status": (request.approvalStatus + 1)
            })
        });
    
        const body = await httpResponse.json();
        console.log(body);
            if (body) {
                alert("Request Successfully Approved!")
                location.reload();
            } else {
                alert("Request Failed to be Approved.")
            }
    }
}

async function reject(request) {
    return async function() {
        const httpResponse = await fetch(`http://localhost:5000/requests/${request.rId}`, {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "status": -1
            })
        });
    
        const body = await httpResponse.json();
        console.log(body);
            if (body) {
                alert("Request Successfully Rejected!")
                location.reload();
            } else {
                alert("Request Failed to be Rejected.")
            }
    }
}

async function submitRequest() {
    let descVal = document.getElementById("descInput").value;
    let costVal = document.getElementById("costInput").value;
    let locationVal = document.getElementById("locationInput").value;
    let dateVal = document.getElementById("dateInput").value;
    let timeVal = document.getElementById("timeInput").value;
    let eventVal = document.getElementById("eventInput").value;

    var unixtime = Date.parse(`${dateVal} ${timeVal}`)/1000;
    
    const params = new URLSearchParams(window.location.search);
    const eId = params.get("eId");

    let request = {
        "employeeId": eId,
        "approvalStatus": 0,
        "datetime": unixtime,
        "location": locationVal,
        "desc": descVal,
        "cost": costVal,
        "gradingId": eventVal,
        "eventTypeId": eventVal
    }

    await fetch(`http://localhost:5000/requests`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request)
    }).then(response => {
        if (response.ok) {
            alert("Request Successfully Added!")
            return response.json()
        } else if(response.status === 422) {
            return Promise.reject('You cannot submit a request at maximum reimbursement.')
        } else {
            return Promise.reject('Error submitting request: ' + response.status)
        }
    })
    .catch(error => alert(error));
}

async function submitDocument(request) {
    let descVal = document.getElementById("descInput").value;
    let gradeVal = document.getElementById("gradeInput").value;
    
    let doc = {
        "desc": descVal,
        "grade": gradeVal,
        "requestId": request.rId,
    }

    const httpResponse = await fetch(`http://localhost:5000/documents`, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(doc)
    });

    const body = await httpResponse.json();
    console.log(body);
    if (body) {
        alert("Document Successfully Added!")
        location.reload();
    } else {
        alert("Document Failed to be added.")
    }
}

function approvalCodeToWords(status) {
    switch(status) {
        case -1:
            return "Rejected"
        case 0:
            return "No Approval"
        case 1:
            return "Super Approved"
        case 2:
            return "Dep Head Approved"
        case 3:
            return "Fully Approved"
    }

}