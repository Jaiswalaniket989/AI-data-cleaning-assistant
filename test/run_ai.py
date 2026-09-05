from src.data_loader import load_dataset
from src.profiler import profile_dataset
from src.anomaly_detector import detect_all_anomalies
from src.ai_assistant import generate_ai_recommendations


def main():

    # Load data
    df = load_dataset(
        "data/input/sample_sales.csv"
    )

    # Profile dataset
    profile = profile_dataset(df)

    # Detect issues
    issues = detect_all_anomalies(df)

    print("\n========== DETECTED ISSUES ==========\n")

    for issue in issues:
        print(issue)

    # AI analysis
    print("\n========== AI ANALYSIS ==========\n")

    recommendations = generate_ai_recommendations(
        issues,
        profile
    )

    print(
        recommendations.get(
            "summary",
            "No summary available."
        )
    )

    print("\nRecommendations:\n")

    for recommendation in recommendations.get(
        "recommendations",
        []
    ):

        print(
            f"\nIssue: "
            f"{recommendation.get('issue_type')}"
        )

        print(
            f"Column: "
            f"{recommendation.get('column')}"
        )

        print(
            f"Severity: "
            f"{recommendation.get('severity')}"
        )

        print(
            f"Action: "
            f"{recommendation.get('recommended_action')}"
        )

        print(
            f"Reason: "
            f"{recommendation.get('reason')}"
        )

        print(
            f"Confidence: "
            f"{recommendation.get('confidence')}"
        )


if __name__ == "__main__":
    main()