import plotly.graph_objects as go

def build_ecr_r_chart_mobile(anxious_score: float, avoidant_score: float, secure_score: float):

    ########### axes ############
    scale_min = 1
    scale_max = 7
    scale_mid = (scale_min + scale_max) / 2

    extra_point_coords = {
        "anxiety": anxious_score,
        "avoidance": avoidant_score,
        "text": f"({round(anxious_score, 2)}, {round(avoidant_score, 2)})",
    }

    xp = extra_point_coords["anxiety"]
    yp = extra_point_coords["avoidance"]

    fig = go.Figure()

    plot_range_min = 0
    plot_range_max = 8

    # anxiety axis
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_mid,
        x1=scale_max,
        y1=scale_mid,
        line=dict(width=2),
    )

    # avoidance axis
    fig.add_shape(
        type="line",
        x0=scale_mid,
        y0=scale_min,
        x1=scale_mid,
        y1=scale_max,
        line=dict(width=2),
    )

    # secure - fearful-avoidant axis
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_min,
        x1=scale_max,
        y1=scale_max,
        line=dict(width=1, dash="dash"),
    )

    # dismissive-preoccupied axis
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_max,
        x1=scale_max,
        y1=scale_min,
        line=dict(width=1, dash="dash"),
    )

    ########### ticks #########

    # ticks values, markers and labels
    tick_values = list(range(scale_min, scale_max + 1))
    tick_marker_style = dict(size=6, color="gray")
    tick_label_font_style = dict(size=10)

    # anxiety ticks
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

    # avoidance ticks
    fig.add_trace(
        go.Scatter(
            x=[scale_mid] * len(tick_values),
            y=tick_values,
            mode="markers+text",
            marker=tick_marker_style,
            text=["1", "2", "3", "", "5", "6", "7"],
            textposition="middle right",
            textfont=tick_label_font_style,
            hoverinfo="none",
        )
    )

    # secure - fearful-avoidant ticks
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

    ############# axis labels ############
    axis_label_font_style = dict(size=12)
    fig.add_annotation(
        x=scale_min - 0.7,
        y=scale_mid,
        text="low anxiety",
        showarrow=False,
        xanchor="center",
        yanchor="middle",
        font=axis_label_font_style,
        textangle=-90,
    )
    fig.add_annotation(
        x=scale_max + 0.7,
        y=scale_mid,
        text="high anxiety",
        showarrow=False,
        xanchor="center",
        yanchor="middle",
        font=axis_label_font_style,
        textangle=-90,
    )
    fig.add_annotation(
        x=scale_mid,
        y=scale_min - 0.7,
        text="low avoidance",
        showarrow=False,
        yanchor="middle",
        xanchor="center",
        textangle=0,
        font=axis_label_font_style,
    )
    fig.add_annotation(
        x=scale_mid,
        y=scale_max + 0.5,
        text="high avoidance",
        showarrow=False,
        yanchor="middle",
        xanchor="center",
        textangle=0,
        font=axis_label_font_style,
    )
    style_label_font_style = dict(size=12, color="green")
    fig.add_annotation(
        x=scale_min - 0.4,
        y=scale_min - 0.7,
        text="<i>secure</i>",
        showarrow=False,
        xanchor="center",
        yanchor="middle",
        font=style_label_font_style,
        textangle=0,
    )
    fig.add_annotation(
        x=scale_max + 0.2,
        y=scale_min - 0.7,
        text="<i>preoccupied</i>",
        showarrow=False,
        xanchor="center",
        yanchor="middle",
        font=style_label_font_style,
        textangle=0,
    )
    fig.add_annotation(
        x=scale_min - 0.1,
        y=scale_max + 0.5,
        text="<i>dismissive</i>",
        showarrow=False,
        xanchor="center",
        font=style_label_font_style,
    )
    fig.add_annotation(
        x=scale_max,
        y=scale_max + 0.5,
        text="<i>fearful-avoidant</i>",
        showarrow=False,
        xanchor="center",
        font=style_label_font_style,
    )

    # score point
    fig.add_trace(
        go.Scatter(
            x=[xp],
            y=[yp],
            mode="markers",
            marker=dict(color="red", size=8, symbol="diamond"),
            text=[extra_point_coords["text"]],
            textposition="bottom left",
            hoverinfo="text",
            textfont=dict(size=12),
        )
    )

    ######### projection lines #########
    projection_line_style = dict(color="rgba(255,0,0,0.5)", width=1, dash="dot")

    # anxiety projection
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

    # avoidance projection
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

    # secure - fearful-avoidant projection
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

    ######### layout ###########
    fig.update_layout(
        title=dict(
            text=f"Anxious: {round(anxious_score, 2)}, "
                 f"Avoidant: {round(avoidant_score, 2)}, "
                 f"Secure: {round(secure_score, 2)}",
            font=dict(color="red", size=12, weight=600),
            pad=dict(b=0),
            xanchor="center",
            x=0.5,
            y=0.97,
        ),
        xaxis=dict(
            range=[plot_range_min, plot_range_max],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            range=[plot_range_min, plot_range_max],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            scaleanchor="x",
            scaleratio=1,
        ),
        width=330,
        height=330,
        margin=dict(l=0, r=0, b=0, t=30),
        showlegend=False,
    )

    # invert y-axis (low avoidance at top [y=1], high avoidance at bottom [y=7])
    fig.update_yaxes(autorange="reversed")

    return fig


def build_ecr_r_chart_desktop(anxious_score: float, avoidant_score: float, secure_score: float):

    ########### axes ############
    scale_min = 1
    scale_max = 7
    scale_mid = (scale_min + scale_max) / 2  # This will be 4

    extra_point_coords = {
        "anxiety": anxious_score,
        "avoidance": avoidant_score,
        "text": f"({round(anxious_score, 2)}, {round(avoidant_score, 2)})",
    }

    xp = extra_point_coords["anxiety"]
    yp = extra_point_coords["avoidance"]

    fig = go.Figure()

    plot_range_min = 0
    plot_range_max = 8

    # anxiety axis
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_mid,
        x1=scale_max,
        y1=scale_mid,
        line=dict(width=2),
    )

    # avoidance axis
    fig.add_shape(
        type="line",
        x0=scale_mid,
        y0=scale_min,
        x1=scale_mid,
        y1=scale_max,
        line=dict(width=2),
    )

    # secure - fearful-avoidant axis
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_min,
        x1=scale_max,
        y1=scale_max,
        line=dict(width=1, dash="dash"),
    )

    # dismissive - preoccupied axis
    fig.add_shape(
        type="line",
        x0=scale_min,
        y0=scale_max,
        x1=scale_max,
        y1=scale_min,
        line=dict(width=1, dash="dash"),
    )

    ############# ticks #############

    # ticks values, markers and labels
    tick_values = list(range(scale_min, scale_max + 1))
    tick_marker_style = dict(size=6, color="gray")
    tick_label_font_style = dict(size=16)

    # anxiety ticks
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

    # avoidance ticks
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

    # secure fearful-avoidant ticks
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

    ########## axis labels #############
    axis_label_font_style = dict(size=16)
    fig.add_annotation(
        x=scale_min - 0.7,
        y=scale_mid,
        text="low anxiety",
        showarrow=False,
        xanchor="center",
        yanchor="middle",
        font=axis_label_font_style,
        textangle=-90,
    )
    fig.add_annotation(
        x=scale_max + 0.7,
        y=scale_mid,
        text="high anxiety",
        showarrow=False,
        xanchor="center",
        yanchor="middle",
        font=axis_label_font_style,
        textangle=-90,
    )
    # Avoidance Axis Labels
    fig.add_annotation(
        x=scale_mid,
        y=scale_min - 0.5,
        text="low avoidance",
        showarrow=False,
        yanchor="middle",
        xanchor="center",
        textangle=0,
        font=axis_label_font_style,
    )
    fig.add_annotation(
        x=scale_mid,
        y=scale_max + 0.5,
        text="high avoidance",
        showarrow=False,
        yanchor="middle",
        xanchor="center",
        textangle=0,
        font=axis_label_font_style,
    )
    style_label_font_style = dict(size=16, color="green")
    fig.add_annotation(
        x=scale_min - 0.4,
        y=scale_min - 0.5,
        text="<i>secure</i>",
        showarrow=False,
        xanchor="center",
        yanchor="middle",
        font=style_label_font_style,
        textangle=0,
    )
    fig.add_annotation(
        x=scale_max + 0.2,
        y=scale_min - 0.5,
        text="<i>preoccupied</i>",
        showarrow=False,
        xanchor="center",
        yanchor="middle",
        font=style_label_font_style,
        textangle=0,
    )
    fig.add_annotation(
        x=scale_min - 0.1,
        y=scale_max + 0.5,
        text="<i>dismissive</i>",
        showarrow=False,
        xanchor="center",
        font=style_label_font_style,
    )
    fig.add_annotation(
        x=scale_max,
        y=scale_max + 0.5,
        text="<i>fearful-avoidant</i>",
        showarrow=False,
        xanchor="center",
        font=style_label_font_style,
    )

    # score point
    fig.add_trace(
        go.Scatter(
            x=[xp],
            y=[yp],
            mode="markers",
            marker=dict(color="red", size=8, symbol="diamond"),
            text=[extra_point_coords["text"]],
            textposition="bottom left",
            hoverinfo="text",
            textfont=dict(size=12),
        )
    )

    ################# projection lines ################
    projection_line_style = dict(color="rgba(255,0,0,0.5)", width=1, dash="dot")

    # anxiety projection
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

    # avoidance projection
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

    # secure -fearful-avoidant projection
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

    ############# layout ################
    fig.update_layout(
        title=dict(
            text=f"Anxious: {round(anxious_score, 2)}, "
                 f"Avoidant: {round(avoidant_score, 2)}, "
                 f"Secure: {round(secure_score, 2)}",
            font=dict(color="red", size=16, weight=700),
            pad=dict(b=0),
            xanchor="center",
            x=0.5,
            y=0.99,
        ),
        xaxis=dict(
            range=[plot_range_min, plot_range_max],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            range=[plot_range_min, plot_range_max],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            scaleanchor="x",
            scaleratio=1,
        ),
        width=800,
        height=800,
        margin=dict(l=0, r=0, b=0, t=30),
        showlegend=False,
    )

    # invert y-axis (low avoidance at top [y=1], high avoidance at bottom [y=7])
    fig.update_yaxes(autorange="reversed")

    return fig
