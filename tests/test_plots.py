import pytest

from attachment_style.attachment_style_test import(
    build_matplotlib_2d_plot,
    build_plotly_3d_plot
    ) 

# Define a fixture for the test data
@pytest.fixture
def plot_data():
    number_of_questions: int = 14
    anxious_score: float = [5]
    secure_score: float = [8]
    avoidant_score: float = [11]
    return {
        "number_of_questions": number_of_questions,
        "anxious_score": anxious_score,
        "secure_score": secure_score,
        "avoidant_score": avoidant_score
    }

def test_matplotlib_2d_plot(plot_data) -> None:
    # build the plot with the data provided by the fixture
    plot = build_matplotlib_2d_plot(
        number_of_questions=plot_data["number_of_questions"],
        anxious_score=plot_data["anxious_score"],
        secure_score=plot_data["secure_score"],
        avoidant_score=plot_data["avoidant_score"]
    )
    plot.show()
    
def test_plotly_3d_plot(plot_data) -> None:
    # build the plot with the data provided by the fixture
    plot = build_plotly_3d_plot(
        number_of_questions=plot_data["number_of_questions"],
        anxious_score=plot_data["anxious_score"],
        secure_score=plot_data["secure_score"],
        avoidant_score=plot_data["avoidant_score"]
    )
    plot.show()
