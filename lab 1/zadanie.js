use music_service_db

db.tracks.insertMany([
    {
        trackId: 101,
        title: "Bohemian Rhapsody",
        artist: "Queen",
        duration: 354,
        genre: "Rock",
        plays: 1500000,
        tags: ["rock", "classic", "legend"],
        album: { title: "A Night at the Opera", year: 1975 }
    },
    {
        trackId: 102,
        title: "Blinding Lights",
        artist: "The Weeknd",
        duration: 200,
        genre: "Pop",
        plays: 2800000,
        tags: ["pop", "synthwave", "top100"],
        album: { title: "After Hours", year: 2020 }
    },
    {
        trackId: 103,
        title: "Shape of You",
        artist: "Ed Sheeran",
        duration: 233,
        genre: "Pop",
        plays: 3100000,
        tags: ["pop", "acoustic", "hit"],
        album: { title: "÷ (Divide)", year: 2017 }
    },
    {
        trackId: 104,
        title: "Smells Like Teen Spirit",
        artist: "Nirvana",
        duration: 301,
        genre: "Rock",
        plays: 1900000,
        tags: ["rock", "grunge", "90s"],
        album: { title: "Nevermind", year: 1991 }
    },
    {
        trackId: 105,
        title: "Stay",
        artist: "The Kid LAROI & Justin Bieber",
        duration: 141,
        genre: "Pop",
        plays: 950000,
        tags: ["pop", "billboard", "short"],
        album: { title: "F*CK LOVE 3", year: 2021 }
    },
    {
        trackId: 106,
        title: "Hotel California",
        artist: "Eagles",
        duration: 390,
        genre: "Rock",
        plays: 1200000,
        tags: ["rock", "classic", "guitar"],
        album: { title: "Hotel California", year: 1976 }
    },
    {
        trackId: 107,
        title: "Bad Guy",
        artist: "Billie Eilish",
        duration: 194,
        genre: "Pop",
        plays: 1700000,
        tags: ["pop", "dark pop", "hit"],
        album: { title: "When We All Fall Asleep...", year: 2019 }
    },
    {
        trackId: 108,
        title: "Stairway to Heaven",
        artist: "Led Zeppelin",
        duration: 482,
        genre: "Rock",
        plays: 1100000,
        tags: ["rock", "classic", "ballad"],
        album: { title: "Led Zeppelin IV", year: 1971 }
    },
    {
        trackId: 109,
        title: "Levitating",
        artist: "Dua Lipa",
        duration: 203,
        genre: "Pop",
        plays: 1400000,
        tags: ["pop", "disco", "dance"],
        album: { title: "Future Nostalgia", year: 2020 }
    },
    {
        trackId: 110,
        title: "Numb",
        artist: "Linkin Park",
        duration: 187,
        genre: "Alternative",
        plays: 1600000,
        tags: ["rock", "alternative", "2000s"],
        album: { title: "Meteora", year: 2003 }
    }
])