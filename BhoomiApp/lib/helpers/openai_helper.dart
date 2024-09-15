import 'package:http/http.dart' as http;
import 'dart:convert';

class OpenAIHelper {
  static const String openAiApiKey = 'YOUR_OPENAI_API_KEY'; // Add your OpenAI API key here

  static Future<String> getGeneratedResponse(String prompt) async {
    final response = await http.post(
      Uri.parse('https://api.openai.com/v1/completions'),
      headers: {
        'Authorization': 'Bearer $openAiApiKey',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 150,
        "temperature": 0.7,
      }),
    );

    if (response.statusCode == 200) {
      var decodedResponse = jsonDecode(response.body);
      return decodedResponse['choices'][0]['text'];
    } else {
      throw Exception('Failed to generate response from OpenAI');
    }
  }
}
