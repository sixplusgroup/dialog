package emotion.controller;

import emotion.service.StaffService;
import emotion.utils.AudioUtil;
import emotion.utils.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/staff")
public class StaffController {
    @Autowired
    private StaffService staffService;

    @PostMapping(value = "/change_staff_voice_print",headers = "content-type=multipart/form-data")
    public Response changeStaffVoicePrint(@RequestParam("CSSId")String CSSId , @RequestParam("file") MultipartFile file) throws IOException {
        return staffService.changeStaffVoicePrint(CSSId,file);
    }
    @PostMapping(value="/add_template",headers = "content-type=multipart/form-data")
    public Response addTemplate(@RequestParam("type")String type , @RequestParam("theme")String theme ,@RequestParam("content")String content) throws IOException {
        return staffService.addTemplate(type,theme,content);
    }

    @PostMapping(value = "/add_staff",headers = "content-type=multipart/form-data")
    public Response addStaff(@RequestParam("name")String name, @RequestParam("file") MultipartFile file) throws IOException {
        return staffService.addStaff(name,file);
    }

    @GetMapping("/get_all_CSStaff")
    public Response getAllStaffCardBaseInfos(){
        return staffService.getAllStaffCardBaseInfos();
    }

    @GetMapping("/get_CSStaff_by_id")
    public Response getCSStaffById(@RequestParam("staffId") Long staffId){
        return staffService.getCSStaffById(staffId);
    }

    @GetMapping("/get_staff_evaluation_by_staff_id")
    public Response getStaffEvaluationByStaffId(@RequestParam("staffId") Long staffId){
        return staffService.getStaffEvaluationByStaffId(staffId);
    }

    @GetMapping("/get_staff_history_scores")
    public Response getStaffHistoryScores(@RequestParam("staffId") Long staffId){
        return staffService.getStaffHistoryScores(staffId);
    }
}
