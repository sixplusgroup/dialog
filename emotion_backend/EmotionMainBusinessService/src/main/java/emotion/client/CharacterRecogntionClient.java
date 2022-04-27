package emotion.client;

import CharacterRecognitionService.CharacterRecognitionService;
import org.apache.thrift.transport.TTransportException;

public class CharacterRecogntionClient extends AbstractClient{
    private CharacterRecognitionService.Client client;
    public void init() throws TTransportException {
        super.init();
        client = new CharacterRecognitionService.Client(protocol);
    }

    public String test(){
        try {
            open();
            return client.test();
        }catch (Exception e){
            e.printStackTrace();
            return null;
        }finally {
            close();
        }
    }
}
