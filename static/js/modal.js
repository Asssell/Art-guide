// Fetch genres from API and display them
fetch('/api/genres')
    .then(response => response.json())
    .then(genres => {
        const genreContainer = document.getElementById('genre-cards');
        genres.forEach(genre => {
            const genreCard = document.createElement('div');
            genreCard.className = 'genre-card';
            genreCard.innerHTML = `
                <img src="${genre.image}" alt="${genre.name}">
                <h3>${genre.name}</h3>
                <p>${genre.description}</p>
            `;
            genreContainer.appendChild(genreCard);
        });
    });

// Fetch artists from API and display them
fetch('/api/artists')
    .then(response => response.json())
    .then(artists => {
        const artistContainer = document.getElementById('artist-cards');
        artists.forEach(artist => {
            const artistCard = document.createElement('div');
            artistCard.className = 'artist-card';
            artistCard.innerHTML = `
                <img src="${artist.image}" alt="${artist.name}">
                <h3>${artist.name}</h3>
                <p>${artist.bio}</p>
            `;
            artistContainer.appendChild(artistCard);
        });
    });

 
