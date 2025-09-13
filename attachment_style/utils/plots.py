import plotly.graph_objects as go

def build_ecr_r_chart(anxious_score: float, avoidant_score: float, secure_score: float):
    # Set default renderer to browser
    # pio.renderers.default = "browser"

    # --- Define the 1-7 scale parameters ---
    scale_min = 1
    scale_max = 7
    scale_mid = (scale_min + scale_max) / 2  # This will be 4

    # --- USER INPUT: Define your extra point's coordinates here (on the 1-7 scale) ---
    # Anxiety: 1 (low) to 7 (high)
    # Avoidance: 1 (low, top of plot) to 7 (high, bottom of plot)
    # Ensure the point is not directly on the main axes (x=4, y=4) or the y=x diagonal
    # for clear projection lines.
    extra_point_coords = {
        "anxiety": anxious_score,
        "avoidance": avoidant_score,
        "text": f"({round(anxious_score, 1)}, {round(avoidant_score, 1)})",
    }
    # --- END USER INPUT ---

    xp = extra_point_coords["anxiety"]
    yp = extra_point_coords["avoidance"]

    # Create the figure
    fig = go.Figure()

    # Define plot range to give some space around the 1-7 scale
    plot_range_min = 0
    plot_range_max = 8

    # 1. Draw Main Conceptual Axes (Anxiety and Avoidance)
    # Horizontal Anxiety Axis (conceptually at y=scale_mid)
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_mid,
        x1=scale_max,
        y1=scale_mid,
        line=dict(width=2),
    )

    # Vertical Avoidance Axis (conceptually at x=scale_mid)
    fig.add_shape(
        type="line",
        x0=scale_mid,
        y0=scale_min,
        x1=scale_mid,
        y1=scale_max,
        line=dict(width=2),
    )

    # 2. Draw Diagonal Axes
    # Secure (1,1) to Fearful-Avoidant (7,7)
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_min,
        x1=scale_max,
        y1=scale_max,
        line=dict(width=1, dash="dash"),
    )
    # Dismissive (1,7) to Preoccupied (7,1)
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_max,
        x1=scale_max,
        y1=scale_min,
        line=dict(width=1, dash="dash"),
    )

    # 3. Add Ticks (dots) and Labels for Axes
    tick_values = list(range(scale_min, scale_max + 1))
    tick_marker_style = dict(size=6, color="gray")
    tick_label_font_style = dict(size=10)

    # Anxiety Axis Ticks (on the line y=scale_mid)
    fig.add_trace(
        go.Scatter(
            x=tick_values,
            y=[scale_mid] * len(tick_values),
            mode="markers+text",
            marker=tick_marker_style,
            text=["1", "2", "3", "", "5", "6", "7"],
            textposition="bottom center",
            textfont=tick_label_font_style,
            hoverinfo="none",
        )
    )

    # Avoidance Axis Ticks (on the line x=scale_mid)
    fig.add_trace(
        go.Scatter(
            x=[scale_mid] * len(tick_values),
            y=tick_values,
            mode="markers+text",
            marker=tick_marker_style,
            text=["1", "2", "3", "", "5", "6", "7"],
            textposition="middle right",  # Adjusted for y-axis ticks
            textfont=tick_label_font_style,
            hoverinfo="none",
        )
    )

    # Secure - Fearful-Avoidant Diagonal Ticks (on the line y=x)
    fig.add_trace(
        go.Scatter(
            x=tick_values,
            y=tick_values,
            mode="markers+text",
            marker=tick_marker_style,
            text=[str(val) for val in tick_values[::-1]],
            textposition="top right",  # Adjust as needed for diagonal
            textfont=tick_label_font_style,
            hoverinfo="none",
        )
    )

    # 4. Add Axis Labels (Low/High)
    axis_label_font_style = dict(size=12)
    # Anxiety Axis Labels
    fig.add_annotation(
        x=scale_min - 0.5,
        y=scale_mid - 0.25,
        text="low anxiety",
        showarrow=False,
        xanchor="center",
        font=axis_label_font_style,
    )
    fig.add_annotation(
        x=scale_max + 0.5,
        y=scale_mid - 0.25,
        text="high anxiety",
        showarrow=False,
        xanchor="center",
        font=axis_label_font_style,
    )
    # Avoidance Axis Labels
    fig.add_annotation(
        x=scale_mid + 0.5,
        y=scale_min,
        text="low avoidance",
        showarrow=False,
        yanchor="middle",
        xanchor="left",
        textangle=0,
        font=axis_label_font_style,
    )
    fig.add_annotation(
        x=scale_mid + 0.5,
        y=scale_max,
        text="high avoidance",
        showarrow=False,
        yanchor="middle",
        xanchor="left",
        textangle=0,
        font=axis_label_font_style,
    )
    # Secure-Fearful-Avoidant Axis Label (Optional - can get crowded)
    # fig.add_annotation(x=scale_max, y=scale_max + 0.3, text="Secure-Fearful", showarrow=False, font=dict(size=10))
    # 5. Add Attachment Style Labels in Quadrants
    style_label_font_style = dict(size=14)
    fig.add_annotation(
        x=scale_min,
        y=scale_min + 0.4,
        text="<i>secure</i>",
        showarrow=False,
        xanchor="right",
        font=style_label_font_style,
    )
    fig.add_annotation(
        x=scale_max,
        y=scale_min + 0.4,
        text="<i>preoccupied</i>",
        showarrow=False,
        xanchor="left",
        font=style_label_font_style,
    )
    fig.add_annotation(
        x=scale_min,
        y=scale_max - 0.4,
        text="<i>dismissive</i>",
        showarrow=False,
        xanchor="right",
        font=style_label_font_style,
    )
    fig.add_annotation(
        x=scale_max,
        y=scale_max - 0.4,
        text="<i>fearful-avoidant</i>",
        showarrow=False,
        xanchor="left",
        font=style_label_font_style,
    )

    # add the legend of the results
    fig.add_annotation(
        x=scale_mid,
        y=scale_min - 1,
        text=f"Your anxious score: {round(anxious_score, 2)}, "
             f"Your avoidant score: {round(avoidant_score, 2)}, "
             f"Your secure score: {round(secure_score, 2)}",
        showarrow=False,
        yanchor="middle",
        xanchor="center",
        textangle=0,
        font={"size": 16, "weight": "bold"},
    )

    # 6. Add the Extra Point
    fig.add_trace(
        go.Scatter(
            x=[xp],
            y=[yp],
            mode="markers",
            marker=dict(color="red", size=12, symbol="diamond"),
            text=[extra_point_coords["text"]],
            textposition="bottom left",
            hoverinfo="text",
            textfont=dict(size=12),
        )
    )

    # 7. Add Projection Lines for the Extra Point
    projection_line_style = dict(color="rgba(255,0,0,0.5)", width=1, dash="dot")

    # Projection to Anxiety Axis (horizontal line at y=scale_mid)
    proj_anxiety_x = xp
    proj_anxiety_y = scale_mid
    fig.add_shape(
        type="line",
        x0=xp,
        y0=yp,
        x1=proj_anxiety_x,
        y1=proj_anxiety_y,
        line=projection_line_style,
    )
    fig.add_trace(
        go.Scatter(
            x=[proj_anxiety_x],
            y=[proj_anxiety_y],
            mode="markers",
            marker=dict(
                color=projection_line_style["color"], size=5, symbol="circle-open"
            ),
            hoverinfo="none",
        )
    )

    # Projection to Avoidance Axis (vertical line at x=scale_mid)
    proj_avoidance_x = scale_mid
    proj_avoidance_y = yp
    fig.add_shape(
        type="line",
        x0=xp,
        y0=yp,
        x1=proj_avoidance_x,
        y1=proj_avoidance_y,
        line=projection_line_style,
    )
    fig.add_trace(
        go.Scatter(
            x=[proj_avoidance_x],
            y=[proj_avoidance_y],
            mode="markers",
            marker=dict(
                color=projection_line_style["color"], size=5, symbol="circle-open"
            ),
            hoverinfo="none",
        )
    )

    # Projection to Secure-Fearful-Avoidant Diagonal (y=x)
    # Formula for projection point: ((xp + yp) / 2, (xp + yp) / 2)
    proj_diag_x = (xp + yp) / 2
    proj_diag_y = (xp + yp) / 2
    fig.add_shape(
        type="line",
        x0=xp,
        y0=yp,
        x1=proj_diag_x,
        y1=proj_diag_y,
        line=projection_line_style,
    )
    fig.add_trace(
        go.Scatter(
            x=[proj_diag_x],
            y=[proj_diag_y],
            mode="markers",
            marker=dict(
                color=projection_line_style["color"], size=5, symbol="circle-open"
            ),
            hoverinfo="none",
        )
    )

    # Update layout
    fig.update_layout(
        xaxis=dict(
            range=[plot_range_min, plot_range_max],
            showgrid=False,
            zeroline=False,
            showticklabels=False,  # We are drawing our own ticks/labels
            title_text="Anxiety Dimension",  # Hidden but good for context
        ),
        yaxis=dict(
            range=[plot_range_min, plot_range_max],
            showgrid=False,
            zeroline=False,
            showticklabels=False,  # We are drawing our own ticks/labels
            title_text="Avoidance Dimension",  # Hidden but good for context
            scaleanchor="x",  # Ensures aspect ratio is 1:1
            scaleratio=1,
        ),
        width=800,
        height=800,
        margin=dict(l=50, r=50, b=50, t=50),
        showlegend=False,
        # plot_bgcolor="white",
        # paper_bgcolor="white",
    )

    # Invert y-axis (low avoidance at top [y=1], high avoidance at bottom [y=7])
    fig.update_yaxes(autorange="reversed")

    return fig

