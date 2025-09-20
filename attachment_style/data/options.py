attachment_style_options = {
    "Avoidant Score": "avoidant_score",
    "Secure Score": "secure_score",
    "Anxious Score": "anxious_score",
}

demographics_options = {
    "Gender": "gender",
    "Therapy Experience": "therapy_experience",
    "Relationship Status": "relationship_status",
}

demographics_values = {
    "gender": ("male", "female", "other"),
    "therapy_experience": ("extensive", "some", "none"),
    "relationship_status": ("married", "in_relationship", "single"),
}

# fmt: off
attachment_style_labels_values = ( 
    {"label": "Anxious", "value": "anxious_score"},
    {"label": "Secure", "value": "secure_score"},
    {"label": "Avoidant", "value": "avoidant_score"},
)

attachment_score_labels_values = (
    {"label": "Anxious Score", "value": "anxious_score"},
    {"label": "Secure Score", "value": "secure_score"},
    {"label": "Avoidant Score", "value": "avoidant_score"},
)
# fmt: on

demographics_labels_values = (
    {"label": "Gender", "value": "gender"},
    {"label": "Therapy Experience", "value": "therapy_experience"},
    {"label": "Relationship Status", "value": "relationship_status"},
)

demographics_radio_options = [
    ["gender", "Gender"],
    ["therapy_experience", "Therapy Experience"],
    ["relationship_status", "Relationship Status"],
]


therapy_labels_values = [
    {"label": "Extensive", "value": "extensive"},
    {"label": "Some", "value": "some"},
    {"label": "None", "value": "none"},
]


gender_labels_values = [
    {"label": "Male", "value": "male"},
    {"label": "Female", "value": "female"},
    {"label": "Other", "value": "other"},
]


relationship_labels_values = [
    {"label": "Single", "value": "single"},
    {"label": "In a relationship", "value": "in_relationship"},
    {"label": "Married", "value": "married"},
]

