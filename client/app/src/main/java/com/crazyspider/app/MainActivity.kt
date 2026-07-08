package com.crazyspider.app

import android.content.ActivityNotFoundException
import android.content.Intent
import android.os.Bundle
import android.speech.RecognizerIntent
import android.speech.tts.TextToSpeech
import android.widget.EditText
import android.widget.ImageButton
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.Locale
import java.util.concurrent.TimeUnit

class MainActivity : AppCompatActivity(), TextToSpeech.OnInitListener {

    private lateinit var recyclerChat: RecyclerView
    private lateinit var editInput: EditText
    private lateinit var btnVoice: ImageButton
    private lateinit var btnSend: ImageButton
    private lateinit var chatAdapter: ChatAdapter
    private var tts: TextToSpeech? = null
    private val messages = mutableListOf<ChatMessage>()
    private val client = OkHttpClient.Builder()
        .connectTimeout(30, TimeUnit.SECONDS)
        .readTimeout(60, TimeUnit.SECONDS)
        .build()

    private val serverUrl = "http://10.0.2.2:8080/api/chat"

    companion object {
        private const val REQ_CODE_SPEECH_INPUT = 100
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        tts = TextToSpeech(this, this)

        recyclerChat = findViewById(R.id.recyclerChat)
        editInput = findViewById(R.id.editInput)
        btnVoice = findViewById(R.id.btnVoice)
        btnSend = findViewById(R.id.btnSend)

        chatAdapter = ChatAdapter(messages, tts)
        recyclerChat.layoutManager = LinearLayoutManager(this)
        recyclerChat.adapter = chatAdapter

        btnVoice.setOnClickListener { startVoiceInput() }
        btnSend.setOnClickListener { sendMessage() }
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            tts?.language = Locale.CHINESE
            addBotMessage("你好，我是 CrazySpider 助手，请用语音或文字向我提问。")
        }
    }

    private fun startVoiceInput() {
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.CHINESE)
            putExtra(RecognizerIntent.EXTRA_PROMPT, getString(R.string.speak_now))
        }
        try {
            startActivityForResult(intent, REQ_CODE_SPEECH_INPUT)
        } catch (e: ActivityNotFoundException) {
            Toast.makeText(this, "您的设备不支持语音输入", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == REQ_CODE_SPEECH_INPUT && resultCode == RESULT_OK && data != null) {
            val results = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            val spokenText = results?.get(0) ?: return
            editInput.setText(spokenText)
            sendMessage()
        }
    }

    private fun sendMessage() {
        val text = editInput.text.toString().trim()
        if (text.isEmpty()) return

        addUserMessage(text)
        editInput.text.clear()

        CoroutineScope(Dispatchers.IO).launch {
            try {
                val reply = callServer(text)
                withContext(Dispatchers.Main) {
                    addBotMessage(reply)
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    addBotMessage("抱歉，请求失败: ${e.message}")
                }
            }
        }
    }

    private fun callServer(message: String): String {
        val json = JSONObject().apply {
            put("message", message)
        }
        val body = json.toString().toRequestBody("application/json".toMediaType())
        val request = Request.Builder()
            .url(serverUrl)
            .post(body)
            .build()

        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) {
                throw Exception("服务器返回错误: ${response.code}")
            }
            val responseBody = response.body?.string() ?: throw Exception("服务器无响应")
            return JSONObject(responseBody).optString("reply", "服务器返回空内容")
        }
    }

    private fun addUserMessage(text: String) {
        messages.add(ChatMessage(text, true))
        chatAdapter.notifyItemInserted(messages.size - 1)
        recyclerChat.scrollToPosition(messages.size - 1)
    }

    private fun addBotMessage(text: String) {
        messages.add(ChatMessage(text, false))
        chatAdapter.notifyItemInserted(messages.size - 1)
        recyclerChat.scrollToPosition(messages.size - 1)

        tts?.let {
            it.language = Locale.CHINESE
            it.speak(text, TextToSpeech.QUEUE_FLUSH, null, "bot_${messages.size}")
        }
    }

    override fun onDestroy() {
        tts?.stop()
        tts?.shutdown()
        super.onDestroy()
    }
}
