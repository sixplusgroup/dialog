package emotion.utils;

import io.micrometer.core.instrument.util.StringUtils;
import org.apache.tomcat.util.http.fileupload.IOUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;

@Component
public class AudioUtil {
    public static boolean saveAudio(String CSSId, MultipartFile file ,String fileSavePath) throws IOException {
        //输入输出流
        OutputStream fileOutputStream = null;
        InputStream inputStream;
        try {
            File outputFile = new File(fileSavePath);
            fileOutputStream = new FileOutputStream(outputFile);
            inputStream = file.getInputStream();
            IOUtils.copy(inputStream, fileOutputStream);
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        } finally {
            //文件操作结束时关闭文件
            if (fileOutputStream != null) {
                fileOutputStream.flush();
                fileOutputStream.close();
            }
        }
        return true;
    }
}
