RECOMMENDATIONS = {
    "fair": {
        "makeup": {
            "foundation": [
                "Light Neutral",
                "Light Beige"
            ],
            "blush": [
                "Peach",
                "Soft Rose"
            ],
            "lipstick": [
                "Nude",
                "Rose",
                "Soft Pink"
            ],
            "eyeshadow": [
                "Brown",
                "Champagne",
                "Soft Taupe"
            ]
        },
        "clothing": [
            "Cream",
            "Navy",
            "Dusty Rose",
            "Olive",
            "Brown"
        ],
        "hijab": [
            "Cream",
            "Dusty Pink",
            "Mauve",
            "Taupe",
            "Soft Brown"
        ]
    },

    "light": {
        "makeup": {
            "foundation": [
                "Light Beige",
                "Neutral Beige"
            ],
            "blush": [
                "Peach",
                "Coral",
                "Rose"
            ],
            "lipstick": [
                "Nude",
                "Coral",
                "Rose"
            ],
            "eyeshadow": [
                "Brown",
                "Gold",
                "Champagne"
            ]
        },
        "clothing": [
            "Beige",
            "Camel",
            "Olive",
            "Navy",
            "Dusty Blue"
        ],
        "hijab": [
            "Beige",
            "Camel",
            "Olive",
            "Dusty Blue",
            "Mauve"
        ]
    },

    "dark": {
        "makeup": {
            "foundation": [
                "Deep Neutral",
                "Deep Warm"
            ],
            "blush": [
                "Terracotta",
                "Berry",
                "Warm Rose"
            ],
            "lipstick": [
                "Berry",
                "Burgundy",
                "Terracotta",
                "Deep Rose"
            ],
            "eyeshadow": [
                "Bronze",
                "Copper",
                "Deep Brown"
            ]
        },
        "clothing": [
            "Emerald",
            "Burgundy",
            "Navy",
            "Mustard",
            "Terracotta"
        ],
        "hijab": [
            "Emerald",
            "Burgundy",
            "Navy",
            "Mustard",
            "Terracotta"
        ]
    }
}


def get_recommendations(skin_tone):
    return RECOMMENDATIONS.get(
        skin_tone,
        {}
    )