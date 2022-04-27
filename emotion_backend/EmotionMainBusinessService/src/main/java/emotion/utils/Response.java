package emotion.utils;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class Response {
    private Integer code;
    private String message;
    private Object data;

    public Response(Integer code, String message, Object data) {
       this.code=code;
       this.message=message;
       this.data=data;
    }
}
