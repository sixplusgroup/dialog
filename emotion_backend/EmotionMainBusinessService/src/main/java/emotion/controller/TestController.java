package emotion.controller;

import emotion.client.CharacterRecogntionClient;
import emotion.client.EmotionRecognitionClient;
import emotion.utils.AudioUtil;
import emotion.utils.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/test")
public class TestController {
    @Autowired
    EmotionRecognitionClient emotionRecognitionClient;
    @Autowired
    CharacterRecogntionClient characterRecogntionClient;

    @GetMapping("/thrift")
    public Response test(){
        return new Response(200,"success","null");
    }
}
