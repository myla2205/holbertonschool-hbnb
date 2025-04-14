/* ======= Login Functions ======= */

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const errorMessage = document.getElementById('error-message');
  const loginButton = document.getElementById('login-button');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      // Clear any previous error messages
      errorMessage.style.display = 'none';

      // Show loading state
      loginButton.disabled = true;
      const originalButtonText = loginButton.textContent;
      loginButton.innerHTML = '<span class="loading-spinner"></span>Logging in...';

      try {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        await loginUser(email, password);
      } catch (error) {
        // Display error message
        errorMessage.textContent = error.message || 'An error occurred during login. Please try again.';
        errorMessage.style.display = 'block';
      } finally {
        // Reset button state
        loginButton.disabled = false;
        loginButton.innerHTML = originalButtonText;
      }
    });
  }

  // Check if we're on the place details page
  if (window.location.pathname.endsWith('place.html')) {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');

    if (placeId) {
      fetchPlaceDetails(token, placeId);
    } else {
      window.location.href = 'index.html';
    }
  }

  // Always check authentication status
  checkAuthentication();
});

async function loginUser(email, password) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Invalid credentials');
    }

    // Store JWT token in cookie
    document.cookie = `token=${data.access_token}; path=/; max-age=86400`; // 86400 seconds = 1 day

    // Redirect to main page
    window.location.href = 'index.html';
  } catch (error) {
    throw error;
  }
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const addReviewSection = document.getElementById('add-review');

  if (token) {
    // User is logged in
    if (loginLink) {
      loginLink.textContent = 'Logout';
      loginLink.href = '#';
      loginLink.onclick = (e) => {
        e.preventDefault();
        logout();
      };
    }
    if (addReviewSection) {
      addReviewSection.style.display = 'block';
    }
    // Fetch places data if the user is authenticated
    fetchPlaces(token);
    return true;
  } else {
    // User is not logged in
    if (loginLink) {
      loginLink.textContent = 'Login';
      loginLink.href = 'login.html';
    }
    if (addReviewSection) {
      addReviewSection.style.display = 'none';
    }
    return false;
  }
}

function logout() {
  document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  window.location.href = 'login.html';
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2)
    return parts.pop().split(';').shift();
  return null;
}


/* ======= All Places Functions =======*/


async function fetchPlaces(token) {
  // Make a GET request to fetch places data
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaces function
  fetch('http://localhost:5000/api/v1/places/', {
    headers: { Authorization: `Bearer ${token}` }
  })
    .then(response => response.json())
    .then(data => displayPlaces(data));
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

  places.forEach(place => {
    const placeDiv = document.createElement('div');
    placeDiv.className = 'place-card';
    placeDiv.dataset.price = place.price;

    placeDiv.innerHTML = `
      <div class="place-info-index">
        <h2 class="place-title">${place.title}</h2>
        <div class="place-details">
          <p class="place-price"><span>Price per night:</span> $${place.price}</p>
        </div>
        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
      </div>
    `;

    placesList.appendChild(placeDiv);
  });

  // Store places data for filtering
  window.placesData = places;
  setupPriceFilter();
}

function setupPriceFilter() {
  const priceFilter = document.getElementById('price-filter');

  priceFilter.addEventListener('change', (event) => {
    let selectedPrice;
    if (event.target.value === 'all') {
      selectedPrice = Infinity;
    } else {
      selectedPrice = parseInt(event.target.value);
    }

    const places = document.querySelectorAll('.place-card');

    places.forEach(place => {
      const price = parseInt(place.dataset.price);
      if (price <= selectedPrice) {
        place.style.display = 'block';
      } else {
        place.style.display = 'none';
      }
    });
  });
}



/* ======= Specific Places Details Functions ======= */

function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  const placeId = urlParams.get('id');
  if (!placeId) {
    console.error('No place ID found in URL');
    window.location.href = 'index.html';
    return null;
  }
  return placeId;
}

async function fetchPlaceDetails(token, placeId) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: headers
    });

    if (!response.ok) {
      throw new Error('Failed to fetch place details');
    }

    const data = await response.json();
    displayPlaceDetails(data);
  } catch (error) {
    console.error('Error fetching place details:', error);
    // Handle error - maybe show an error message to the user
    const placeDetails = document.getElementById('place-details');
    placeDetails.innerHTML = '<p class="error">Error loading place details. Please try again later.</p>';
  }
}

function displayPlaceDetails(place) {
  // Display place details
  const placeDetails = document.getElementById('place-details');

  // Handle host name
  let hostName = 'Unknown';
  if (place.owner) {
    hostName = `${place.owner.first_name} ${place.owner.last_name}`;
  }

  // Handle amenities
  let amenitiesHtml = '';
  if (place.amenities) {
    amenitiesHtml = `<p><strong>Amenities:</strong> ${place.amenities.map(amenity => amenity.name).join(', ')}</p>`;
  }

  placeDetails.innerHTML = `
    <h1>${place.title}</h1>
    <div class="place-info">
      <p><strong>Host:</strong> ${hostName}</p>
      <p><strong>Price:</strong> $${place.price} per night</p>
      <p><strong>Description:</strong> ${place.description}</p>
      ${amenitiesHtml}
    </div>
  `;

  // Display reviews
  const reviewsContainer = document.getElementById('reviews-container');
  reviewsContainer.innerHTML = '';

  if (place.reviews && place.reviews.length > 0) {
    place.reviews.forEach(review => {
      const reviewElement = document.createElement('div');
      reviewElement.className = 'review-card';

      // Create star rating HTML
      let stars = '';
      for (let i = 0; i < 5; i++) {
        let starClass = '';
        if (i < review.rating) {
          starClass = ' checked';
        }
        stars += `<span class="fa fa-star${starClass}"></span>`;
      }

      // Handle reviewer name
      let reviewerName = 'Anonymous';
      if (review.user && review.user.first_name && review.user.last_name) {
        reviewerName = `${review.user.first_name} ${review.user.last_name}`;
      }

      reviewElement.innerHTML = `
        <p><strong>${reviewerName}:</strong></p>
        <p>${review.text}</p>
        <p>Rating: ${stars}</p>
      `;
      reviewsContainer.appendChild(reviewElement);
    });
  } else {
    reviewsContainer.innerHTML = '<p>No reviews yet.</p>';
  }

  // Handle review form visibility
  const addReviewSection = document.getElementById('add-review');
  const token = getCookie('token');
  if (token) {
    addReviewSection.style.display = 'block';
  } else {
    addReviewSection.style.display = 'none';
  }
}




/* ======= Add Review Functions ======= */

document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  if (reviewForm) {
    // Fetch place details to update the title
    fetchPlaceTitle(token, placeId);

    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const reviewText = reviewForm.elements['review-text'].value.trim();
      const rating = reviewForm.elements['rating'].value;

      if (!reviewText || !rating) {
        alert('Please fill in all fields before submitting.');
        return;
      }

      try {
        await submitReview(token, placeId, reviewText, rating);
        reviewForm.reset();
      } catch (error) {
        console.error('Error:', error);
        alert(error.message || 'Failed to submit review');
      }
    });
  }
});

async function fetchPlaceTitle(token, placeId) {
  try {
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Failed to fetch place details');

    const titleElement = document.getElementById('place-title');
    if (titleElement) titleElement.textContent = data.title || 'Unknown Place';
  } catch (error) {
    console.error('Error fetching place details:', error);
  }
}

async function submitReview(token, placeId, reviewText, rating) {
  const endpoint = `http://localhost:5000/api/v1/places/${placeId}/reviews`;
  const requestBody = {
    'text': reviewText,
    'rating': parseInt(rating, 10)
  };

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(requestBody)
    });

    if (response.ok) {
      alert('Review submitted successfully!');
      document.getElementById('review-form').reset();
    } else {
      const errorData = await response.json();
      alert(`Failed to submit review: ${errorData.message}`);
    }
  } catch (error) {
    alert(`An error occurred: ${error.message}`);
  }
}