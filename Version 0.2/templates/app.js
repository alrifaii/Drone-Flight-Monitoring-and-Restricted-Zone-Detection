// Initialize the map centered on Vienna
const map = L.map('map').setView([48.2082, 16.3738], 13);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Store markers and path
const markers = {};
let pathLine = null;
let showPath = true;

// Function to update locations
function updateLocations() {
    fetch('/get_locations')
        .then(response => response.json())
        .then(data => {
            // Clear old markers not in new data
            Object.keys(markers).forEach(id => {
                if (!data.some(loc => loc.id == id)) {
                    map.removeLayer(markers[id]);
                    delete markers[id];
                }
            });

            // Add new markers
            data.forEach(location => {
                if (!markers[location.id]) {
                    markers[location.id] = L.marker([location.lat, location.lng], {
                        riseOnHover: true
                    }).addTo(map)
                        .bindPopup(createPopupContent(location))
                        .on('click', () => showLocationInfo(location));
                }
            });

            // Update the connecting path
            updatePathLine(data);

            // Update history list
            updateHistoryList(data);
        });
}

// Update the connecting path line
function updatePathLine(locations) {
    // Remove existing path if it exists
    if (pathLine) {
        map.removeLayer(pathLine);
    }

    // Only draw path if we have at least 2 points and path is enabled
    if (locations.length >= 2 && showPath) {
        const segments = [];
        let currentSegment = {
            points: [[locations[0].lat, locations[0].lng]],
            color: locations[0].permission === '✅ Flying allowed' ? '#2ecc71' : '#e74c3c'
        };

        // Group consecutive points with same permission status
        for (let i = 1; i < locations.length; i++) {
            const currentColor = locations[i].permission === '✅ Flying allowed' ? '#2ecc71' : '#e74c3c';

            if (currentColor === currentSegment.color) {
                currentSegment.points.push([locations[i].lat, locations[i].lng]);
            } else {
                segments.push(currentSegment);
                currentSegment = {
                    points: [[locations[i-1].lat, locations[i-1].lng], [locations[i].lat, locations[i].lng]],
                    color: currentColor
                };
            }
        }
        segments.push(currentSegment); // Add the last segment

        // Draw each segment with its appropriate color
        segments.forEach(segment => {
            L.polyline(segment.points, {
                color: segment.color,
                weight: 4,
                opacity: 0.7,
                lineJoin: 'round'
            }).addTo(map);
        });
    }
}

// Toggle path visibility
window.togglePath = function() {
    showPath = !showPath;
    updateLocations();
};

// Create popup content
function createPopupContent(location) {
    return `
        <strong>Location #${location.id}</strong><br>
        <b>Time:</b> ${location.time}<br>
        <b>Coordinates:</b><br>
        Lat: ${location.lat.toFixed(6)}<br>
        Lng: ${location.lng.toFixed(6)}<br>
        <b>Permission:</b> ${location.permission}
    `;
}

// Show location info in panel
function showLocationInfo(location) {
    document.getElementById('location-info').innerHTML = `
        <h4>Location #${location.id}</h4>
        <p><b>Time recorded:</b> ${location.time}</p>
        <p><b>Latitude:</b> ${location.lat.toFixed(6)}</p>
        <p><b>Longitude:</b> ${location.lng.toFixed(6)}</p>
        <p><b>Distance from center:</b> ${calculateDistance(location).toFixed(2)} km</p>
        <p><b>Permission:</b> ${location.permission}</p>
    `;
}

// Calculate distance from Vienna center
function calculateDistance(location) {
    const R = 6371; // Earth radius in km
    const dLat = (location.lat - 48.2082) * Math.PI / 180;
    const dLng = (location.lng - 16.3738) * Math.PI / 180;
    const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(48.2082 * Math.PI / 180) * Math.cos(location.lat * Math.PI / 180) * 
        Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
}

// Update history list
function updateHistoryList(locations) {
    const historyList = document.getElementById('history-list');
    historyList.innerHTML = '';

    locations.slice().reverse().forEach(location => {
        const item = document.createElement('div');
        item.className = 'history-item';
        item.innerHTML = `
            <span class="location-id">#${location.id}</span>
            <span class="location-permission">${location.permission}</span>
            <span class="location-time">${location.time}</span>
            <button onclick="flyToLocation(${location.lat}, ${location.lng})">View</button>
        `;
        historyList.appendChild(item);
    });
}

// Fly to location
window.flyToLocation = function(lat, lng) {
    map.flyTo([lat, lng], 15);
};

// Update locations every second
setInterval(updateLocations, 1000);
updateLocations(); // Initial load
