
attachment_style_options: dict[str, str] = {
    "Avoidant Score": "avoidant_score",
    "Secure Score": "secure_score",
    "Anxious Score": "anxious_score",
}

demographics_options: dict[str, str] = {
    "Gender": "gender",
    "Therapy Experience": "therapy_experience",
    "Relationship Status": "relationship_status",
}

demographics_values: dict[str, tuple[str, ...]] = {
    "gender": ("male", "female", "other"),
    "therapy_experience": ("extensive", "some", "none"),
    "relationship_status": ("married", "in_relationship", "single"),
}

# fmt: off
attachment_style_labels_values: tuple[dict[str, str], ...] = ( 
    {"label": "Anxious", "value": "anxious_score"},
    {"label": "Secure", "value": "secure_score"},
    {"label": "Avoidant", "value": "avoidant_score"},
)

attachment_score_labels_values: tuple[dict[str, str], ...] = (
    {"label": "Anxious Score", "value": "anxious_score"},
    {"label": "Secure Score", "value": "secure_score"},
    {"label": "Avoidant Score", "value": "avoidant_score"},
)
# fmt: on

demographics_labels_values: tuple[dict[str, str], ...] = (
    {"label": "Gender", "value": "gender"},
    {"label": "Therapy Experience", "value": "therapy_experience"},
    {"label": "Relationship Status", "value": "relationship_status"},
)
