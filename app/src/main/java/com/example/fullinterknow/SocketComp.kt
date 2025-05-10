package com.example.fullinterknow
import android.util.Log
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import java.io.IOException

object SocketComp { // Keep using SocketComp as the object, even though we are now doing HTTP
    private val client = OkHttpClient()

    // ... (remove Socket.IO connection code if you are fully switching to HTTP for this interaction)

    fun sendHttpRequestToFlask(message: String, callback: (String?) -> Unit) {
        val mediaType = "application/json; charset=utf-8".toMediaType()
        val requestBody = """
            {
                "message": "$message"
            }
        """.trimIndent().toRequestBody(mediaType)

        // Replace with your Flask server's IP and port (same as you used for Socket.IO testing)
        val flaskEndpointUrl = "http://10.20.3.189:5000/test" // Ensure port 5000 if Flask is on 5000

        val request = Request.Builder()
            .url(flaskEndpointUrl)
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(object : okhttp3.Callback {
            override fun onFailure(call: okhttp3.Call, e: IOException) {
                Log.e("SocketComp", "HTTP request to Flask failed: ${e.message}", e)
                callback(null) // Indicate failure
            }

            override fun onResponse(call: okhttp3.Call, response: okhttp3.Response) {
                val responseBody = response.body?.string()
                if (response.isSuccessful) {
                    Log.d("SocketComp", "HTTP request to Flask successful, response: $responseBody")
                    callback(responseBody) // Pass the response back to the callback
                } else {
                    Log.e("SocketComp", "HTTP request to Flask failed with code: ${response.code}, message: ${responseBody}")
                    callback(null) // Indicate failure
                }
                response.close() // Important to close the response body
            }
        })
    }
}
