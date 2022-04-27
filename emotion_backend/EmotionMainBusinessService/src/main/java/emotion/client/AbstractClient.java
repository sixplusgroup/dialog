package emotion.client;

import EmotionRecognitionService.EmotionRecognitionService;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;

public abstract class AbstractClient {
    protected TBinaryProtocol protocol;
    private TTransport transport;
    private String host;
    private int port;

    public void setHost(String host) {
        this.host = host;
    }

    public void setPort(int port) {
        this.port = port;
    }

    public void init() throws TTransportException {
        transport = new TSocket(host, port);
        protocol = new TBinaryProtocol(transport);
    }

    protected void open() throws TTransportException {
        transport.open();
    }

    protected void close()
    {
        transport.close();
    }
}
