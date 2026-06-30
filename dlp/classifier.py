BUSINESS_KEYWORDS = {

    "confidential_project": [
        "roadmap",
        "prototype",
        "secret",
        "acquisition"
    ],

    "source_code": [
        "class ",
        "private key",
        "token",
        "password"
    ],

    "customer_data": [
        "customer",
        "client",
        "invoice"
    ]
}


def classify_business(text):

    matches = []

    lower = text.lower()

    for category, words in BUSINESS_KEYWORDS.items():

        for word in words:

            if word.lower() in lower:

                matches.append(category)

                break

    return matches