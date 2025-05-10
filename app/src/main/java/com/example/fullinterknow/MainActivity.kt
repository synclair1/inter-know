package com.example.fullinterknow

import android.Manifest
import android.app.Activity
import android.content.ContentUris
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.provider.AlarmClock
import android.provider.ContactsContract
import android.speech.RecognizerIntent
import android.telephony.TelephonyManager
import android.util.Log
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.MutableState
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.example.fullinterknow.ui.theme.FullInterknowTheme
import androidx.navigation.NavHost
import androidx.navigation.compose.rememberNavController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.platform.LocalContext
import androidx.core.content.ContextCompat
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FieldValue
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.Query
import io.socket.client.IO
import io.socket.client.Socket
import org.json.JSONObject
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import kotlinx.coroutines.*

data class ChatMessage(
    val author: String,
    val message: String,
    val time: String
)
val auth= FirebaseAuth.getInstance()
val database = FirebaseFirestore.getInstance()

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            FullInterknowTheme {
                var personname = remember { mutableStateOf("") }
                var roomname = remember { mutableStateOf("")}
                val navController = rememberNavController()
                NavHost(navController, startDestination = "register") {
                    composable("login") { LoginPage(navController) }
                    composable("register") { RegisterPage(navController) }
                    composable("roomselect"){ RoomPage(navController,personname,roomname)}
                    composable("chat/{roomId}") { backStackEntry ->
                        val roomId = backStackEntry.arguments?.getString("roomId") ?: ""
                        ChatPage(roomId,personname.value)  // Pass room ID to ChatPage
                    }

                }
            }
        }
    }
}
val MessageList= mutableStateListOf(ChatMessage("Chat Assistant","How're you doing?","14:36"),
    )
fun setAlarm(context: Context, hours: Int, minutes: Int){
    val intent= Intent(AlarmClock.ACTION_SET_ALARM).apply{
        putExtra(AlarmClock.EXTRA_HOUR,hours)
        putExtra(AlarmClock.EXTRA_MINUTES,minutes)
        addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
    }
    context.startActivity(intent)
    if (intent.resolveActivity(context.packageManager) != null) {
        try {
            context.startActivity(intent)
        } catch (e: Exception) {
            Log.e("AlarmManager", "Error starting alarm intent", e)
        }
    } else {
        Log.e("AlarmManager", "No app found to handle alarm intent")
    }
}
fun ReminderManager(context: Context, message: String, hours: Int, minutes: Int){
    val intent= Intent(AlarmClock.ACTION_SET_ALARM).apply{
        putExtra(AlarmClock.EXTRA_MESSAGE,message)
        putExtra(AlarmClock.EXTRA_HOUR,hours)
        putExtra(AlarmClock.EXTRA_MINUTES,minutes)
    }
    context.startActivity(intent)
}
fun AppFinder(context: Context,app: String){
    val pm = context.packageManager
    val intent = Intent(Intent.ACTION_MAIN, null)
    intent.addCategory(Intent.CATEGORY_LAUNCHER)

    val apps = pm.queryIntentActivities(intent, 0)
    for (app0 in apps) {
        val label = app0.loadLabel(pm).toString().trim().lowercase()  // Convert to lowercase
        val appNameLower = app.trim().lowercase()  // Convert appName to lowercase
        Log.d("AppFinder", "Found app: $label")

        if (label == appNameLower) {  // Case-insensitive comparison
            val launchIntent = pm.getLaunchIntentForPackage(app0.activityInfo.packageName)
            if (launchIntent != null) {
                context.startActivity(launchIntent)
                return
            }
        }
    }

    Toast.makeText(context, "App \"$app\" not found", Toast.LENGTH_SHORT).show()
}
fun callContactByName(context: Context, targetName: String) {
    val contentResolver = context.contentResolver
    val uri = ContactsContract.CommonDataKinds.Phone.CONTENT_URI
    val projection = arrayOf(
        ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME,
        ContactsContract.CommonDataKinds.Phone.NUMBER
    )

    val cursor = contentResolver.query(
        uri,
        projection,
        null,
        null,
        null
    )

    cursor?.use {
        while (it.moveToNext()) {
            val name = it.getString(0)
            val number = it.getString(1)
            if (name.contains(targetName, ignoreCase = true)) {
                val intent = Intent(Intent.ACTION_DIAL).apply {
                    data = Uri.parse("tel:${Uri.encode(number)}")
                    flags = Intent.FLAG_ACTIVITY_NEW_TASK
                }
                context.startActivity(intent)
                return
            }
        }
        Toast.makeText(context, "No matching contact found", Toast.LENGTH_SHORT).show()
    }
}

fun openContactPageByName(context: Context, targetName: String) {
    val contentResolver = context.contentResolver
    val uri = ContactsContract.Contacts.CONTENT_URI
    val projection = arrayOf(
        ContactsContract.Contacts._ID,
        ContactsContract.Contacts.DISPLAY_NAME
    )

    val cursor = contentResolver.query(
        uri,
        projection,
        null,
        null,
        null
    )

    cursor?.use {
        while (it.moveToNext()) {
            val id = it.getString(0)
            val name = it.getString(1)

            if (name.contains(targetName, ignoreCase = true)) {
                val contactUri = ContentUris.withAppendedId(ContactsContract.Contacts.CONTENT_URI, id.toLong())
                val intent = Intent(Intent.ACTION_VIEW).apply {
                    data = contactUri
                    flags = Intent.FLAG_ACTIVITY_NEW_TASK
                }
                context.startActivity(intent)
                return
            }
        }
        Toast.makeText(context, "No matching contact found", Toast.LENGTH_SHORT).show()
    }
}
//fun canMakeCalls(context: Context): Boolean {
//    val telephonyManager = context.getSystemService(Context.TELEPHONY_SERVICE) as TelephonyManager
//    return telephonyManager.phoneType != TelephonyManager.PHONE_TYPE_NONE
//}
//fun callContactByName(context: Context, contactName: String) {
//    if (!canMakeCalls(context)) {
//        Toast.makeText(context, "This device cannot make calls", Toast.LENGTH_SHORT).show()
//        return
//    }
//
//    // Continue with your existing code to query contacts and make the call
//    val resolver = context.contentResolver
//    val cursor = resolver.query(
//        ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
//        arrayOf(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME, ContactsContract.CommonDataKinds.Phone.NUMBER),
//        ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME + " LIKE ?",
//        arrayOf("%$contactName%"),
//        null
//    )
//
//    if (cursor != null && cursor.moveToFirst()) {
//        val contactNumber = cursor.getString(cursor.getColumnIndex(ContactsContract.CommonDataKinds.Phone.NUMBER))
//        val contactDisplayName = cursor.getString(cursor.getColumnIndex(ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME))
//
//        val intent = Intent(Intent.ACTION_CALL).apply {
//            data = Uri.parse("tel:$contactNumber")
//        }
//        context.startActivity(intent)
//        cursor.close()
//    } else {
//        Toast.makeText(context, "No contact found with name: $contactName", Toast.LENGTH_SHORT).show()
//    }
//}
@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = name,
        fontSize = 32.sp,
        fontWeight = FontWeight.Bold,
        modifier = modifier
    )
}

@Composable
fun TextInput(textog: String) {
    var text = remember { mutableStateOf("") }
    TextField(
        value = text.value,
        onValueChange = { text.value = it },
        label = { Text(textog) },
    )
}

@Composable
fun ButtonFunction(intext: String,onClick: () -> Unit) {
    Button(onClick = onClick)
    {
        Text(intext)
    }
}
@Composable
fun ButtonFunctionRegister(intext: String,onClick: () -> Unit) {
    Button(onClick = onClick)
    {
        Text(intext)
    }
}

@Composable
fun RegisterPage(navController: NavController) {
    var emailState=remember{ mutableStateOf("")}
    var passwordState=remember{ mutableStateOf("")}
    var firstNameState=remember{ mutableStateOf("")}
    var lastNameState=remember{ mutableStateOf("")}
    Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
        Column (
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ){
            Greeting(
                name = "Interknow Registration",
                modifier = Modifier.padding(innerPadding)
            )
            TextField(
                value = emailState.value,
                onValueChange = { emailState.value = it },
                label = { Text("Please enter email...") },
            )
            TextField(
                value = passwordState.value,
                onValueChange = { passwordState.value = it },
                label = { Text("Please enter password...") },

                )
            TextField(
                value = firstNameState.value,
                onValueChange = { firstNameState.value = it },
                label = { Text("Please enter first name...") },
            )
            TextField(
                value = lastNameState.value,
                onValueChange = { lastNameState.value = it },
                label = { Text("Please enter last name...") },

                )
            ButtonFunction("Register"){
                val email=emailState.value
                val password=passwordState.value
                val firstName=firstNameState.value
                val lastName=lastNameState.value
                auth.createUserWithEmailAndPassword(email, password)
                    .addOnCompleteListener { task ->
                        if (task.isSuccessful) {
                            val user = auth.currentUser
                            val userMap = hashMapOf(
                                "firstName" to firstName,
                                "lastName" to lastName,
                                "email" to email
                            )
                            user?.let {
                                database.collection("users").document(it.uid).set(userMap)
                                    .addOnSuccessListener {
                                        Log.d("RegisterPage", "User data saved successfully!")
                                        navController.navigate("roomselect") // Navigate after saving user data
                                    }
                                    .addOnFailureListener { e ->
                                        Log.e("RegisterPage", "Error saving user data: ${e.message}")
                                    }
                            }// Navigate after successful registration
                        } else {
                            Log.e("RegisterPage", "Registration failed: ${task.exception?.message}")
                        }
                    }
            }
            Spacer(modifier = Modifier.height(16.dp))

            // Button to navigate back to Login
            ButtonFunction("Go to Login") {
                navController.navigate("login")
            }
        }
    }
}

@Composable
fun LoginPage(navController: NavController) {
    var emailState=remember{ mutableStateOf("")}
    var passwordState=remember{ mutableStateOf("")}
    Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
        Column (
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ){
            Greeting(
                name = "Interknow Login",
                modifier = Modifier.padding(innerPadding)
            )
            TextField(
                value = emailState.value,
                onValueChange = { emailState.value = it },
                label = { Text("Please enter email...") },
                )
            TextField(
                value = passwordState.value,
                onValueChange = { passwordState.value = it },
                label = { Text("Please enter password...") },

                )
            ButtonFunction("Login"){
                val email = emailState.value
                val password= passwordState.value
                auth.signInWithEmailAndPassword(email,password)
                    .addOnCompleteListener { task ->
                        if (task.isSuccessful) {
                            val user = auth.currentUser
                            navController.navigate("roomselect") // Navigate after successful registration
                        } else {
                            Log.e("LoginPage", "Login failed: ${task.exception?.message}")
                        }
                    }
            }
            Spacer(modifier = Modifier.height(16.dp))

            // Button to navigate back to Login
            ButtonFunction("Go to Register") {
                navController.navigate("register")
            }
        }
    }
}
@Composable
fun RoomPage(navController: NavController,personname: MutableState<String>,roomname: MutableState<String>){
    val current=auth.currentUser
    val context = LocalContext.current
    var rooms = remember { mutableStateOf(listOf<Pair<String,String>>()) }
    LaunchedEffect (current){ current?.let{user->
        database.collection("users").document(user.uid).collection("Rooms")
            .get()
            .addOnSuccessListener { querySnapshot ->
                rooms.value = querySnapshot.documents.mapNotNull {
                    val roomname = it.getString("roomname") // Get room name
                    val roomId = it.id
                    if (roomname != null) Pair(roomname, roomId) else null
                } }
            .addOnFailureListener { e->
                Toast.makeText(context, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
    }}
    Row(modifier=Modifier.fillMaxSize().horizontalScroll(rememberScrollState())){
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = "Your Rooms",
                style = MaterialTheme.typography.titleLarge,
                modifier = Modifier.padding(bottom = 8.dp)
            )
            LazyColumn {
                items(rooms.value) { (roomname,roomId) ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp)
                            .clickable { navController.navigate("chat/$roomId") },
                            elevation = CardDefaults.elevatedCardElevation(defaultElevation = 4.dp)
                    ) {
                        Text(
                            text = roomname,
                            style = MaterialTheme.typography.bodyLarge,
                            modifier = Modifier
                                .padding(16.dp)
                        )
                    }
                }
            }
        }
        Column (
            modifier = Modifier.fillMaxSize(),
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally,

        ){
            Greeting(
                name = "Create a new chat",
                modifier = Modifier.padding(5.dp),


                )
            TextField(
                value = personname.value,
                onValueChange = { personname.value = it },
                label = { Text("Please enter your name...") },

                )
            TextField(
                value = roomname.value,
                onValueChange = { roomname.value = it },
                label = { Text("Please enter room name...") },

                )

            ButtonFunction("Enter Room"){
                val RoomData= hashMapOf(
                    "roomname" to roomname.value
                )
                current?.let { user ->
                    val userDocRef =
                        database.collection("users").document(user.uid).collection("Rooms")
                            .add(RoomData)
                            .addOnSuccessListener { documentReference ->
                                val roomId = documentReference.id
                                navController.navigate("chat/$roomId")
                            }
                            .addOnFailureListener { e ->
                                Log.e("RoomPage", "Error adding room: ${e.message}")
                            }


                } ?:Log.e("RoomPage", "User is not logged in")


            }
        }
    }
}

@Composable
fun MessageBox(msg:ChatMessage){
    val image = runCatching { painterResource(R.drawable.ic_launcher_background) }
        .getOrElse { painterResource(android.R.drawable.ic_menu_report_image) }
    val BubbleBackgroundColor=if(msg.author=="Chat Assistant"){
        MaterialTheme.colorScheme.primary
    }else{
        MaterialTheme.colorScheme.secondary
    }
    val ChatBubbleShape = if(msg.author=="Chat Assistant") {
        RoundedCornerShape(
            topStart = 16.dp, topEnd = 16.dp, bottomEnd = 16.dp
        )
    }else {
        RoundedCornerShape(
            topStart = 16.dp, topEnd = 16.dp, bottomStart = 16.dp
        )
    }
    val ArrangeCond=if(msg.author=="Chat Assistant"){
        Arrangement.Start
    }else{
        Arrangement.End
    }

    Row (modifier=Modifier
        .padding(all = 8.dp)
        .fillMaxWidth(),
        horizontalArrangement = ArrangeCond){ if (msg.author=="Chat Assistant"){Image(
        painter = image,
        contentDescription = "some guy",
        modifier=Modifier
            .size(40.dp)
            .clip(CircleShape)
            .border(1.5.dp, MaterialTheme.colorScheme.secondary, CircleShape)
    )
        Spacer(modifier = Modifier.width(8.dp))
        Surface( // Wrap only the text bubble
            color = BubbleBackgroundColor,
            shape = ChatBubbleShape,
            modifier = Modifier
                .widthIn(min = 120.dp, max = 300.dp) // Wider bubble
                .heightIn(min = 40.dp) // Slightly taller bubble
                .padding(bottom = 10.dp) // Optional padding inside bubble
        ){
            Column(
                modifier = Modifier
                    .padding(horizontal = 12.dp, vertical = 8.dp)
            ) {
                Text(
                    msg.author,
                    style = MaterialTheme.typography.bodyMedium
                )
                Spacer(Modifier.height(4.dp))
                Text(
                    msg.message,
                    style = MaterialTheme.typography.bodySmall
                )
                Spacer(Modifier.height(4.dp))
                Text(
                    text = msg.time,
                    style = MaterialTheme.typography.labelSmall
                )
            }
        }
    }else{
        Surface(
            color = BubbleBackgroundColor,
            shape = ChatBubbleShape, // Use a mirrored version
            modifier = Modifier
                .widthIn(min = 120.dp, max = 300.dp) // Set width constraints
        ) {
            Column(modifier = Modifier.padding(12.dp)) {
                Text(
                    msg.author,
                    style = MaterialTheme.typography.bodyMedium
                )
                Spacer(Modifier.height(4.dp))
                Text(
                    msg.message,
                    style = MaterialTheme.typography.bodySmall
                )
                Spacer(Modifier.height(4.dp))
                Text(
                    text = msg.time,
                    style = MaterialTheme.typography.labelSmall
                )
            }
        }

        Spacer(modifier = Modifier.width(8.dp)) // Space between bubble and image

        Image(
            painter = image,
            contentDescription = "some guy",
            modifier = Modifier
                .size(40.dp)
                .clip(CircleShape)
                .border(1.5.dp, MaterialTheme.colorScheme.secondary, CircleShape)
        )
    }
    }
}

@Composable
fun MessageInput(roomId: String,personname: String){
    val user=auth.currentUser
    var text=remember{ mutableStateOf("")}
    val context= LocalContext.current
    val voiceInputLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { activityResult ->
        if (activityResult.resultCode == Activity.RESULT_OK) {
            val result = activityResult.data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            text.value = result?.get(0) ?: ""
        }
    }

    fun VoiceInput(){
        val language="en"
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE,language)
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT,"Speak to text")
        try{
            voiceInputLauncher.launch(intent)
        }
        catch(e: Exception){
            Toast.makeText(context, " " + e.message, Toast.LENGTH_SHORT).show()
        }
    }
    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted: Boolean ->
        if (isGranted) {
            // Permission granted, proceed with voice input
            VoiceInput()
        } else {
            // Permission denied
            Toast.makeText(context, "Microphone permission denied", Toast.LENGTH_SHORT).show()
        }
    }
    fun requestVoiceInputWithPermission() {
        if (ContextCompat.checkSelfPermission(context, Manifest.permission.RECORD_AUDIO)
            != PackageManager.PERMISSION_GRANTED
        ) {
            permissionLauncher.launch(Manifest.permission.RECORD_AUDIO)
        } else {
            VoiceInput()
        }
    }
    Column{
    Row (
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp), // Add padding to space the UI nicely
        horizontalArrangement = Arrangement.spacedBy(8.dp), // Adds spacing between the buttons and text field
        verticalAlignment = Alignment.CenterVertically // Aligns buttons and textfield in center
    ){
        TextField(
            value = text.value,
            onValueChange = { text.value = it },
            label = { Text("Please enter message...") },

        )
        ButtonFunction("Send") {
            var textval=text.value
            val lastWord = textval.trim().split("\\s+".toRegex()).lastOrNull() ?: ""
            MessageList.add(ChatMessage(personname, textval, "14:36"))
            val messData= hashMapOf(
                "name" to "Ali",
                "messagetext" to textval,
                "timestamp" to "14:36"
            )
            if (user!=null){

                    database.collection("users").document(user.uid).collection("Rooms").document(roomId).collection("messages").add(messData)

                    // Use HTTP request instead of Socket.IO sendMessage
                    SocketComp.sendHttpRequestToFlask(textval) { flaskResponse ->
                        if (flaskResponse != null) {
                            var fullResponse=flaskResponse
                            Log.d("MessageInput", "Flask response received: $flaskResponse")
                            MessageList.add(ChatMessage("Chat Assistant", flaskResponse, "Backend Time"))
                            val MessData2=hashMapOf(
                                "name" to "Chat Assistant",
                                "messagetext" to flaskResponse,
                                "timestamp" to "Backend Time"
                            )
                            database.collection("users").document(user.uid).collection("Rooms").document(roomId).collection("messages").add(MessData2)
                            GlobalScope.launch(Dispatchers.Main) {
                                delay(3000)
                                when (fullResponse) {
                                    "Setting an alarm." -> {
                                        val timeParts = lastWord.split(":")
                                        if (timeParts.size == 2) {
                                            val hours = timeParts[0].toIntOrNull()
                                            val minutes = timeParts[1].toIntOrNull()
                                            if (hours != null && minutes != null) {
                                                setAlarm(context, hours, minutes)
                                            } else {
                                                Log.e("AlarmManager", "Invalid time format in lastWord: $lastWord")
                                            }
                                        } else {
                                            Log.e("AlarmManager", "Time not in expected format: $lastWord")
                                        }
                                    }

                                    "Opening the application for $lastWord." -> {
                                        AppFinder(context, lastWord)
                                    }
                                    "Setting a reminder."->{
                                        val messageRegex = "'([^']+)'".toRegex()
                                        val timeRegex = "\\b\\d{1,2}:\\d{2}\\b".toRegex()

                                        val message = messageRegex.find(textval)?.groupValues?.get(1) ?: ""
                                        val timeString = timeRegex.find(textval)?.value ?: ""
                                        val timeParts = timeString.split(":")
                                        if (timeParts.size == 2) {
                                            val hours = timeParts[0].toIntOrNull()
                                            val minutes = timeParts[1].toIntOrNull()
                                            if (hours != null && minutes != null) {
                                                ReminderManager(context, message, hours, minutes)
                                            } else {
                                                Log.e("ReminderManager", "Invalid time format: $timeString")
                                            }
                                        } else {
                                            Log.e("ReminderManager", "Time not found or invalid")
                                        }
                                    }
                                    "Sure, I will initiate the call to $lastWord."->{
                                        callContactByName(context,lastWord)
                                    }
                                    "Fetching contact details."->{
                                        openContactPageByName(context,lastWord)
                                    }

                                    else -> {
                                        Log.d("FunctionTrigger", "No matching condition for: $fullResponse")
                                    }
                                }

                        } }else {
                            Log.e("MessageInput", "Failed to get response from Flask")
                            // Handle error case (e.g., show an error message to the user)
                        }
                    }
                }
            }


        }
        ButtonFunction("Voice") {
            requestVoiceInputWithPermission()
        }

    }}

@Composable
fun ChatPage(roomId: String,personname: String){
    val user=auth.currentUser
    val userid=user?.uid?:""
    val context = LocalContext.current
    LaunchedEffect(roomId) {
        val messagesRef = database.collection("users").document(userid).collection("Rooms").document(roomId).collection("messages")
            .orderBy("timestamp", Query.Direction.ASCENDING) // Sort by oldest first

        messagesRef.addSnapshotListener { snapshot, error ->
            if (error != null) {
                Log.e("ChatPage", "Error fetching messages: ${error.message}")
                Toast.makeText(context, "Failed to load messages", Toast.LENGTH_SHORT).show()
                return@addSnapshotListener
            }

            snapshot?.let { querySnapshot ->
                MessageList.clear()
                for (doc in querySnapshot.documents) {
                    val name = doc.getString("name") ?: "Unknown"
                    val messagetext = doc.getString("messagetext") ?: ""
                    val timestamp = doc.getString("timestamp") ?: ""

                    MessageList.add(ChatMessage(name, messagetext, timestamp))
                }
            }
        }
    }
    Column {
        Greeting("New chat", modifier = Modifier.padding(8.dp))
        LazyColumn {
            items(MessageList) { message ->
                MessageBox(message)
            }
        }
        MessageInput(roomId, personname)
    }
}
@Preview(showBackground = true)
@Composable
fun MessageBoxPreview(){
    MaterialTheme{
        MessageBox(ChatMessage("Ali","How are you?","14:36"))
    }

}