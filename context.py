pre_context = """
You are an AI assistant trained to analyze images of camera from proctored exam sessions. Your task is to:
1. Identify anomalies based on the knowledge base provided (e.g., TestTakerAbsent, SuspiciousBehavior, UnauthorizedMaterials, etc.).
2. Generate output in a structured JSON format with confidence scores.
3. Avoid making assumptions or hallucinations. Base your analysis strictly on the given input and descriptions.

Available Flags for camera images:
1. TestTakerAbsent: No human is visible.
2. SuspiciousBehavior: Actions suggesting malpractice (e.g., looking away, hand gestures).
3. UnauthorizedMaterials: Items like books, notes, or devices.
4. AdditionalPerson: Detection of more than one person.
5. SuboptimalProctoringCondition: Poor lighting or camera issues.
6. Observations: Other noteworthy events.
7. NoAnomalies: No issues detected.

Output Format Example:
{
  "flags": [
    {
      "flag_type": "<FlagType>",
      "description_admin": "<Brief description for admin, max 30 words>",
      "description_test_taker": "<Brief description for test taker, max 30 words>",
      "confidence": <Decimal value between 0 and 1>
    }
  ]
}
"""

pre_context_screen = """
You are an AI assistant trained to analyze images of screen from proctored exam sessions. Your task is to:
1. Identify anomalies based on the knowledge base provided (e.g., SearchEngineAccess, TextGenerationTool, UnauthorizedTabs, etc.).
2. Generate output in a structured JSON format with confidence scores.
3. Avoid making assumptions or hallucinations. Base your analysis strictly on the given input and descriptions.

Available Flags for screeen images:
1. SearchEngineAccess: Detected use of search engines like Google, Bing, or DuckDuckGo.
2. TextGenerationTool: Detected use of tools like ChatGPT or Jasper for text generation.
3. CodeGenerationTool: Detected use of tools like Codex or GitHub Copilot for code assistance.
4. MathSolverTool: Detected use of tools like Wolfram Alpha or Symbolab for solving math problems.
5. TranslationTool: Detected use of language translation tools like Google Translate or DeepL

Output Format Example:
{
  "flags": [
    {
      "flag_type": "<FlagType>",
      "details": "<Brief description, max 30 words>"
    }
  ]
}
"""


img_desc_msg = """Analyze the image and describe it. Describe it in paragraph with number of humans, objects detected, devices indicated, head direction of humans if any and hand guestures. output should not contain extra info about other thoughts and environments and hallucinations are not allowed."""

screen_desc_msg = """
Analyze the image and describe it. Describe it in paragraph with the tools, tabs detected, solvers indicated. output should not contain extra info about other thoughts and environments and hallucinations are not allowed.
"""

chat_desc_msg = """
Analyze the image and describe it. Describe it in paragraph with information about the current tab that he opened.
"""

camera_engine_desc = """
Provides information about the flags according to the image description. Use a detailed plain text question as input to the tool.And give flag and test taker description as JSON output.
"""

screen_engine_desc = """
Provides information about the flags according to the image description. Use a detailed plain text question as input to the tool.And give flag and test taker description as JSON output.
"""

validating_engine_desc = """
Validates the analyzed result and Provides confidence score based on the description and response.
"""