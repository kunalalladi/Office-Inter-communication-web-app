var Message= document.getElementById("Message");

Message.addEventListener("click",function(){
    window.location.href="C:\\Users\\HP\\OneDrive\\Desktop\\website\\html_files\\message.html"
});

const searchInput = document.getElementById('searchInput');
const statusTable = document.getElementById('statusTable');
const tableRows = statusTable.getElementsByTagName('tr');

searchInput.addEventListener('input', function () {
  const searchValue = this.value.toLowerCase();

  for (let i = 1; i < tableRows.length; i++) {
    const projectName = tableRows[i].cells[0].textContent.toLowerCase();

    if (projectName.includes(searchValue)) {
      tableRows[i].style.display = '';
    } else {
      tableRows[i].style.display = 'none';
    }
  }
});
function getreq() {
    var x=document.getElementById("req")
    var y=document.getElementById("areq")
    var z=document.getElementById("ped")
    var p=document.getElementById("req1")
    var q=document.getElementById("req2")
    var r=document.getElementById("req3")
    p.style.borderBottom = "3px solid grey";
    q.style.borderBottom = "none";
    r.style.borderBottom = "none";
    x.style.display = "block";
    y.style.display = "none";
    z.style.display = "none";
}
function getareq() {
    var x=document.getElementById("req")
    var y=document.getElementById("areq")
    var z=document.getElementById("ped")
    var p=document.getElementById("req1")
    var q=document.getElementById("req2")
    var r=document.getElementById("req3")
    p.style.borderBottom = "none";
    q.style.borderBottom = "3px solid grey";
    r.style.borderBottom = "none";
    x.style.display = "none";
    y.style.display = "block";
    z.style.display = "none";
}
function getped() {
    var x=document.getElementById("req")
    var y=document.getElementById("areq")
    var z=document.getElementById("ped")
    var p=document.getElementById("req1")
    var q=document.getElementById("req2")
    var r=document.getElementById("req3")
    p.style.borderBottom = "none";
    q.style.borderBottom = "none";
    r.style.borderBottom = "3px solid grey";
    x.style.display = "none";
    y.style.display = "none";
    z.style.display = "block";
}