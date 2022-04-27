package emotion.client;

import EmotionRecognitionService.EmotionRecognitionService;
import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;


public class EmotionRecognitionClient extends AbstractClient{
    private EmotionRecognitionService.Client client;

    public void init() throws TTransportException {
        super.init();
        client = new EmotionRecognitionService.Client(protocol);
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
