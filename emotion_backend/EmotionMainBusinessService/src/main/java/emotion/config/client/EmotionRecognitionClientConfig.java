package emotion.config.client;

import emotion.client.EmotionRecognitionClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class EmotionRecognitionClientConfig {
    @Value("${thrift.EmotionRecognitionService.host}")
    private String host;
    @Value("${thrift.EmotionRecognitionService.port}")
    private int port;

    @Bean(initMethod = "init")
    public EmotionRecognitionClient emotionRecognitionClient(){
        EmotionRecognitionClient emotionRecognitionClient = new EmotionRecognitionClient();
        emotionRecognitionClient.setHost(host);
        emotionRecognitionClient.setPort(port);
        return emotionRecognitionClient;
    }

}
