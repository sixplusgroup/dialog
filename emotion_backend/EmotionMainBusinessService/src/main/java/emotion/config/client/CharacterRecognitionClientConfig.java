package emotion.config.client;

import emotion.client.CharacterRecogntionClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class CharacterRecognitionClientConfig {
    @Value("${thrift.CharacterRecognitionService.host}")
    private String host;
    @Value("${thrift.CharacterRecognitionService.port}")
    private int port;

    @Bean(initMethod = "init")
    public CharacterRecogntionClient characterRecogntionClient(){
        CharacterRecogntionClient characterRecogntionClient = new CharacterRecogntionClient();
        characterRecogntionClient.setHost(host);
        characterRecogntionClient.setPort(port);
        return characterRecogntionClient;
    }
}
