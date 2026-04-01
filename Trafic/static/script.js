let map;
let parkingSlots = 24;

/* ================= NAVIGATION ================= */

function showPage(pageId, element) {

    document.querySelectorAll(".nav-link").forEach(link => {
        link.classList.remove("active");
    });

    if (element) element.classList.add("active");

    document.querySelectorAll(".page-section").forEach(section => {
        section.classList.remove("active");
    });

    document.getElementById(pageId).classList.add("active");

    document.getElementById("dynamic-title").innerText =
        pageId.charAt(0).toUpperCase() + pageId.slice(1);

    if (pageId === "traffic" && !map) initMap();
}

/* ================= UPLOAD + START ================= */

async function startDetection() {

    const videoInput = document.getElementById("videoInput");
    const status = document.getElementById("detectionStatus");
    const liveFeed = document.getElementById("liveFeed");
    const placeholder = document.getElementById("videoPlaceholder");

    if (videoInput.files.length === 0) {
        alert("Upload video first!");
        return;
    }

    let formData = new FormData();
    formData.append("video", videoInput.files[0]);

    status.innerText = "Uploading...";
    status.style.color = "orange";

    await fetch("/upload", {
        method: "POST",
        body: formData
    });

    status.innerText = "Starting Detection...";

    await fetch("/start_detection", {
        method: "POST"
    });

    status.innerText = "Detection Started";
    status.style.color = "lime";

    placeholder.style.display = "none";
    liveFeed.src = "/video_feed";
    liveFeed.style.display = "block";
}

/* ================= LIVE STATS ================= */

setInterval(async () => {

    try {
        const res = await fetch("/stats");
        const data = await res.json();

        document.getElementById("avgSpeed").innerText = data.avgSpeed;
        document.getElementById("totalVehicles").innerText = data.totalVehicles;
        document.getElementById("violationCount").innerText = data.violations;

        document.getElementById("carCount").innerText = data.cars;
        document.getElementById("bikeCount").innerText = data.bikes;
        document.getElementById("busCount").innerText = data.buses;
        document.getElementById("truckCount").innerText = data.trucks;
        document.getElementById("bicycleCount").innerText = data.bicycles;

    } catch (error) {
        console.log("Stats fetch error");
    }

}, 1000);

/* ================= MAP ================= */

function initMap() {

    map = L.map('map').setView([22.5726, 88.3639], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
        .addTo(map);
}

/* ================= LIVE LOCATION ================= */

function addUserLocation() {

    if (!navigator.geolocation) {
        alert("Geolocation not supported");
        return;
    }

    navigator.geolocation.getCurrentPosition(position => {

        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        L.marker([lat, lon])
            .addTo(map)
            .bindPopup("You are here")
            .openPopup();

        map.setView([lat, lon], 15);

    }, () => {
        alert("Location permission denied");
    });
}

/* ================= PARKING ================= */

function generateParking() {

    const grid = document.getElementById("parkingGrid");
    if (!grid) return;

    for (let i = 1; i <= parkingSlots; i++) {

        const slot = document.createElement("div");
        slot.classList.add("slot");
        slot.innerText = "P" + i;

        grid.appendChild(slot);
    }
}

/* ================= ON LOAD ================= */

window.onload = function () {
    generateParking();
};
