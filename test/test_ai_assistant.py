def test_ai_module_import():

    from src.ai_assistant import generate_ai_recommendations

    assert callable(generate_ai_recommendations)