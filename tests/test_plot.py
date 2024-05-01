from attachment_style.attachment_style_test import build_plotly_3d_plot

def main() -> None:    
    # set the parameters
    number_of_questions: int = 14
    anxious_score: float = [5]
    secure_score: float = [8]
    avoidant_score: float = [11]
    
    # build the plot
    build_plotly_3d_plot(
        number_of_questions=number_of_questions,
        anxious_score=anxious_score,
        secure_score=secure_score,
        avoidant_score=avoidant_score
    )

if __name__ == "__main__":
    main()