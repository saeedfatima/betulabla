/ Boreholes Management JavaScript

// Mock data for boreholes
let BOREHOLES = [
    {
        id: 1,
        location: 'Kofar Naisa',
        localGovernment: 'Kano Municipal',
        status: 'operational',
        dateInstalled: '2023-01-15',
        lastServiced: '2023-06-10',
        waterQuality: 'excellent',
        depth: 120,
        fundedBy: 'Betul Abla Donors',
        description: 'Solar-powered borehole serving a community of approximately 500 people.',
        coordinates: {
            latitude: '11.9907',
            longitude: '8.5148'
        },
        maintenanceHistory: [
            {
                id: 1,
                date: '2023-06-10',
                type: 'Routine',
                performedBy: 'Mohammed Abdullahi',
                description: 'Regular maintenance and cleaning of solar panels'
            }
        ],
        images: []
    },
    {
        id: 2,
        location: 'Central Market Area',
        localGovernment: 'Ungogo',
        status: 'operational',
        dateInstalled: '2023-03-22',
        lastServiced: '2023-07-15',
        waterQuality: 'good',
        depth: 95,
        fundedBy: 'Community Association',
        description: 'Hand-pump borehole installed near the central market area.',
        coordinates: {
            latitude: '12.0184',
            longitude: '8.5346'
        },
        maintenanceHistory: [
            {
                id: 1,
                date: '2023-07-15',
                type: 'Repair',
                performedBy: 'Ibrahim Musa',
                description: 'Fixed leaking pipe and replaced hand pump components'
            }
        ],
        images: []
    },
    {
        id: 3,
        location: 'Community Primary School',
        localGovernment: 'Dambatta',
        status: 'maintenance',
        dateInstalled: '2023-06-05',
        lastServiced: '2023-08-20',
        waterQuality: 'fair',
        depth: 110,
        fundedBy: 'Education Development Fund',
        description: 'Borehole serving the primary school and surrounding community.',
        coordinates: {
            latitude: '12.4358',
            longitude: '8.5152'
        },
        maintenanceHistory: [
            {
                id: 1,
                date: '2023-08-20',
                type: 'Maintenance',
                performedBy: 'Aisha Yusuf',
                description: 'Water quality test shows need for filter replacement'
            }
        ],
        images: []
    }
];

// List of Kano State Local Governments
const LOCAL_GOVERNMENTS = [
    'Ajingi', 'Albasu', 'Bagwai', 'Bebeji', 'Bichi', 'Bunkure', 
    'Dala', 'Dambatta', 'Dawakin Kudu', 'Dawakin Tofa', 'Doguwa',
    'Fagge', 'Gabasawa', 'Garko', 'Garum Mallam', 'Gaya', 'Gezawa',
    'Gwale', 'Gwarzo', 'Kabo', 'Kano Municipal', 'Karaye', 'Kibiya',
    'Kiru', 'Kumbotso', 'Kunchi', 'Kura', 'Madobi', 'Makoda', 
    'Minjibir', 'Nasarawa', 'Rano', 'Rimin Gado', 'Rogo', 'Shanono',
    'Sumaila', 'Takai', 'Tarauni', 'Tofa', 'Tsanyawa', 'Tudun Wada',
    'Ungogo', 'Warawa', 'Wudil'
];

// DOM elements
let boreholesTable;
let paginationContainer;
let localGovDropdown;
let statusDropdown;
let yearDropdown;

// Current filters and pagination state
let currentFilters = {
    localGovernment: '',
    status: '',
    year: '',
    search: ''
};
let currentPage = 1;
const itemsPerPage = 10;

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    boreholesTable = document.getElementById('boreholesTable');
    paginationContainer = document.getElementById('pagination');
    localGovDropdown = document.getElementById('filterLGA');
    statusDropdown = document.getElementById('filterStatus');
    yearDropdown = document.getElementById('filterYear');
    
    // Populate local government dropdown
    populateLocalGovernments();
    
    // Populate years dropdown (from 2010 to current year)
    populateYears();
    
    // Set up event listeners
    setupEventListeners();
    
    // Load initial data
    loadBoreholes();
});

// Populate local government dropdown
function populateLocalGovernments() {
    LOCAL_GOVERNMENTS.forEach(lg => {
        const option = document.createElement('option');
        option.value = lg;
        option.textContent = lg;
        localGovDropdown.appendChild(option);
    });
}

// Populate years dropdown
function populateYears() {
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= 2010; year--) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearDropdown.appendChild(option);
    }
}

// Set up event listeners
function setupEventListeners() {
    // Filter buttons
    document.getElementById('applyFilters').addEventListener('click', applyFilters);
    document.getElementById('clearFilters').addEventListener('click', clearFilters);
    
    // Search
    document.getElementById('searchBtn').addEventListener('click', performSearch);
    document.getElementById('searchBoreholes').addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // Add borehole form submission
    document.getElementById('saveBoreholeBtn').addEventListener('click', saveBorehole);
    
    // Update borehole
    document.getElementById('updateBoreholeBtn').addEventListener('click', updateBorehole);
    
    // Check authentication
    checkAuth();
}

// Apply filters to the borehole list
function applyFilters() {
    currentFilters.localGovernment = localGovDropdown.value;
    currentFilters.status = statusDropdown.value;
    currentFilters.year = yearDropdown.value;
    currentPage = 1;
    loadBoreholes();
}

// Clear all filters
function clearFilters() {
    localGovDropdown.value = '';
    statusDropdown.value = '';
    yearDropdown.value = '';
    document.getElementById('searchBoreholes').value = '';
    currentFilters = {
        localGovernment: '',
        status: '',
        year: '',
        search: ''
    };
    currentPage = 1;
    loadBoreholes();
}

// Perform search
function performSearch() {
    const searchTerm = document.getElementById('searchBoreholes').value.trim();
    currentFilters.search = searchTerm;
    currentPage = 1;
    loadBoreholes();
}

// Load and display boreholes based on current filters and pagination
function loadBoreholes() {
    // Apply filters
    let filteredBoreholes = BOREHOLES.filter(borehole => {
        // Local Government filter
        if (currentFilters.localGovernment && borehole.localGovernment !== currentFilters.localGovernment) {
            return false;
        }
        
        // Status filter
        if (currentFilters.status && borehole.status !== currentFilters.status) {
            return false;
        }
        
        // Year filter
        if (currentFilters.year) {
            const installYear = new Date(borehole.dateInstalled).getFullYear().toString();
            if (installYear !== currentFilters.year) {
                return false;
            }
        }
        
        // Search filter
        if (currentFilters.search) {
            const searchTerm = currentFilters.search.toLowerCase();
            return (
                borehole.location.toLowerCase().includes(searchTerm) ||
                borehole.localGovernment.toLowerCase().includes(searchTerm) ||
                borehole.description.toLowerCase().includes(searchTerm)
            );
        }
        
        return true;
    });
    
    // Apply pagination
    const totalPages = Math.ceil(filteredBoreholes.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const paginatedBoreholes = filteredBoreholes.slice(startIndex, startIndex + itemsPerPage);
    
    // Render boreholes
    renderBoreholes(paginatedBoreholes);
    
    // Update pagination
    renderPagination(totalPages);
}

// Render the boreholes table
function renderBoreholes(boreholes) {
    boreholesTable.innerHTML = '';
    
    if (boreholes.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="7" class="text-center">No boreholes found matching the criteria.</td>';
        boreholesTable.appendChild(row);
        return;
    }
    
    boreholes.forEach(borehole => {
        const row = document.createElement('tr');
        
        // Format the status with appropriate badge
        let statusBadge;
        switch(borehole.status) {
            case 'operational':
                statusBadge = '<span class="badge bg-success">Operational</span>';
                break;
            case 'maintenance':
                statusBadge = '<span class="badge bg-warning text-dark">Maintenance Required</span>';
                break;
            case 'non-operational':
                statusBadge = '<span class="badge bg-danger">Non-operational</span>';
                break;
            default:
                statusBadge = '<span class="badge bg-secondary">Unknown</span>';
        }
        
        row.innerHTML = `
            <td>${borehole.id}</td>
            <td>${borehole.location}</td>
            <td>${borehole.localGovernment}</td>
            <td>${statusBadge}</td>
            <td>${formatDate(borehole.dateInstalled)}</td>
            <td>${borehole.lastServiced ? formatDate(borehole.lastServiced) : 'Not serviced'}</td>
            <td>
                <div class="action-buttons">
                    <button class="btn btn-sm btn-primary" onclick="viewBorehole(${borehole.id})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-warning" onclick="editBorehole(${borehole.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteBorehole(${borehole.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        `;
        
        boreholesTable.appendChild(row);
    });
}

// Format a date string to a more readable format
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', options);
}

// Render pagination controls
function renderPagination(totalPages) {
    paginationContainer.innerHTML = '';
    
    if (totalPages <= 1) {
        return;
    }
    
    const ul = document.createElement('ul');
    ul.className = 'pagination';
    
    // Previous button
    const prevLi = document.createElement('li');
    prevLi.className = 'page-item' + (currentPage === 1 ? ' disabled' : '');
    prevLi.innerHTML = `<a class="page-link" href="#" onclick="goToPage(${currentPage - 1}); return false;">Previous</a>`;
    ul.appendChild(prevLi);
    
    // Page buttons
    for (let i = 1; i <= totalPages; i++) {
        const li = document.createElement('li');
        li.className = 'page-item' + (i === currentPage ? ' active' : '');
        li.innerHTML = `<a class="page-link" href="#" onclick="goToPage(${i}); return false;">${i}</a>`;
        ul.appendChild(li);
    }
    
    // Next button
    const nextLi = document.createElement('li');
    nextLi.className = 'page-item' + (currentPage === totalPages ? ' disabled' : '');
    nextLi.innerHTML = `<a class="page-link" href="#" onclick="goToPage(${currentPage + 1}); return false;">Next</a>`;
    ul.appendChild(nextLi);
    
    paginationContainer.appendChild(ul);
}

// Change page
function goToPage(page) {
    currentPage = page;
    loadBoreholes();
    window.scrollTo(0, 0);
}

// View borehole details
function viewBorehole(id) {
    const borehole = BOREHOLES.find(b => b.id === id);
    
    if (!borehole) {
        showNotification('Borehole not found!', 'danger');
        return;
    }
    
    // Populate form with borehole data
    document.getElementById('editBoreholeId').value = borehole.id;
    document.getElementById('editLocation').value = borehole.location;
    document.getElementById('editLocalGovernment').value = borehole.localGovernment;
    document.getElementById('editDateInstalled').value = borehole.dateInstalled;
    document.getElementById('editStatus').value = borehole.status;
    document.getElementById('editWaterQuality').value = borehole.waterQuality || '';
    document.getElementById('editLastServiced').value = borehole.lastServiced || '';
    document.getElementById('editDepth').value = borehole.depth || '';
    document.getElementById('editFundedBy').value = borehole.fundedBy || '';
    document.getElementById('editDescription').value = borehole.description || '';
    
    if (borehole.coordinates) {
        document.getElementById('editLatitude').value = borehole.coordinates.latitude || '';
        document.getElementById('editLongitude').value = borehole.coordinates.longitude || '';
    }
    
    // Populate the maintenance history tab
    const maintenanceTable = document.getElementById('maintenanceTable');
    maintenanceTable.innerHTML = '';
    
    if (borehole.maintenanceHistory && borehole.maintenanceHistory.length > 0) {
        borehole.maintenanceHistory.forEach(record => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${formatDate(record.date)}</td>
                <td>${record.type}</td>
                <td>${record.performedBy}</td>
                <td>${record.description}</td>
                <td>
                    <button class="btn btn-sm btn-danger" onclick="deleteMaintenanceRecord(${borehole.id}, ${record.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            maintenanceTable.appendChild(row);
        });
    } else {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="5" class="text-center">No maintenance records available.</td>';
        maintenanceTable.appendChild(row);
    }
    
    // Populate images tab (placeholder)
    const imagesGrid = document.getElementById('boreholeImagesGrid');
    imagesGrid.innerHTML = '';
    
    if (borehole.images && borehole.images.length > 0) {
        borehole.images.forEach((image, index) => {
            const col = document.createElement('div');
            col.className = 'col-md-4 mb-3';
            col.innerHTML = `
                <div class="card">
                    <div class="bg-light p-3 text-center">
                        <p class="text-muted">[Image ${index + 1}]</p>
                    </div>
                    <div class="card-body">
                        <button class="btn btn-sm btn-danger w-100" onclick="deleteImage(${borehole.id}, ${index})">
                            <i class="fas fa-trash me-1"></i> Remove
                        </button>
                    </div>
                </div>
            `;
            imagesGrid.appendChild(col);
        });
    } else {
        imagesGrid.innerHTML = '<div class="col-12 text-center py-4">No images available.</div>';
    }
    
    // Populate local governments dropdown
    populateEditLocalGovernments(borehole.localGovernment);
    
    // Show the modal
    const boreholeModal = new bootstrap.Modal(document.getElementById('viewBoreholeModal'));
    boreholeModal.show();
}

// Populate the edit form's local government dropdown
function populateEditLocalGovernments(selected) {
    const dropdown = document.getElementById('editLocalGovernment');
    dropdown.innerHTML = '';
    
    LOCAL_GOVERNMENTS.forEach(lg => {
        const option = document.createElement('option');
        option.value = lg;
        option.textContent = lg;
        if (lg === selected) {
            option.selected = true;
        }
        dropdown.appendChild(option);
    });
}

// Edit borehole (same as view but sets up for editing)
function editBorehole(id) {
    viewBorehole(id);
}

// Delete borehole
function deleteBorehole(id) {
    if (confirm('Are you sure you want to delete this borehole?')) {
        BOREHOLES = BOREHOLES.filter(borehole => borehole.id !== id);
        loadBoreholes();
        showNotification('Borehole deleted successfully!', 'success');
    }
}

// Save new borehole
function saveBorehole() {
    const location = document.getElementById('location').value.trim();
    const localGovernment = document.getElementById('localGovernment').value;
    const dateInstalled = document.getElementById('dateInstalled').value;
    const status = document.getElementById('status').value;
    
    if (!location || !localGovernment || !dateInstalled || !status) {
        showNotification('Please fill in all required fields', 'danger');
        return;
    }
    
    // Create new borehole object
    const newBorehole = {
        id: getNextBoreholeId(),
        location,
        localGovernment,
        dateInstalled,
        status,
        waterQuality: document.getElementById('waterQuality').value,
        lastServiced: document.getElementById('lastServiced').value || null,
        depth: document.getElementById('depth').value ? parseFloat(document.getElementById('depth').value) : null,
        fundedBy: document.getElementById('fundedBy').value.trim(),
        description: document.getElementById('description').value.trim(),
        coordinates: {
            latitude: document.getElementById('latitude').value.trim(),
            longitude: document.getElementById('longitude').value.trim()
        },
        maintenanceHistory: [],
        images: []
    };
    
    // Add to boreholes array
    BOREHOLES.unshift(newBorehole);
    
    // Reset form
    document.getElementById('addBoreholeForm').reset();
    
    // Hide modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('addBoreholeModal'));
    modal.hide();
    
    // Reload boreholes
    loadBoreholes();
    
    showNotification('Borehole added successfully!', 'success');
}

// Update existing borehole
function updateBorehole() {
    const id = parseInt(document.getElementById('editBoreholeId').value);
    const boreholeIndex = BOREHOLES.findIndex(b => b.id === id);
    
    if (boreholeIndex === -1) {
        showNotification('Borehole not found!', 'danger');
        return;
    }
    
    const location = document.getElementById('editLocation').value.trim();
    const localGovernment = document.getElementById('editLocalGovernment').value;
    const dateInstalled = document.getElementById('editDateInstalled').value;
    const status = document.getElementById('editStatus').value;
    
    if (!location || !localGovernment || !dateInstalled || !status) {
        showNotification('Please fill in all required fields', 'danger');
        return;
    }
    
    // Update borehole data
    BOREHOLES[boreholeIndex] = {
        ...BOREHOLES[boreholeIndex], // Keep existing data like maintenanceHistory and images
        location,
        localGovernment,
        dateInstalled,
        status,
        waterQuality: document.getElementById('editWaterQuality').value,
        lastServiced: document.getElementById('editLastServiced').value || null,
        depth: document.getElementById('editDepth').value ? parseFloat(document.getElementById('editDepth').value) : null,
        fundedBy: document.getElementById('editFundedBy').value.trim(),
        description: document.getElementById('editDescription').value.trim(),
        coordinates: {
            latitude: document.getElementById('editLatitude').value.trim(),
            longitude: document.getElementById('editLongitude').value.trim()
        }
    };
    
    // Hide modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('viewBoreholeModal'));
    modal.hide();
    
    // Reload boreholes
    loadBoreholes();
    
    showNotification('Borehole updated successfully!', 'success');
}

// Get next borehole ID
function getNextBoreholeId() {
    const ids = BOREHOLES.map(borehole => borehole.id);
    return ids.length > 0 ? Math.max(...ids) + 1 : 1;
}

// Delete maintenance record
function deleteMaintenanceRecord(boreholeId, recordId) {
    if (confirm('Are you sure you want to delete this maintenance record?')) {
        const boreholeIndex = BOREHOLES.findIndex(b => b.id === boreholeId);
        
        if (boreholeIndex !== -1) {
            BOREHOLES[boreholeIndex].maintenanceHistory = BOREHOLES[boreholeIndex].maintenanceHistory.filter(
                record => record.id !== recordId
            );
            
            // Refresh the view
            viewBorehole(boreholeId);
            
            showNotification('Maintenance record deleted successfully!', 'success');
        }
    }
}

// Delete image
function deleteImage(boreholeId, imageIndex) {
    if (confirm('Are you sure you want to delete this image?')) {
        const boreholeIndex = BOREHOLES.findIndex(b => b.id === boreholeId);
        
        if (boreholeIndex !== -1 && BOREHOLES[boreholeIndex].images) {
            BOREHOLES[boreholeIndex].images.splice(imageIndex, 1);
            
            // Refresh the view
            viewBorehole(boreholeId);
            
            showNotification('Image deleted successfully!', 'success');
        }
    }
}

// Show notification/toast message
function showNotification(message, type = 'success') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Create toast content
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Add toast to container
    toastContainer.appendChild(toast);
    
    // Initialize the toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}
