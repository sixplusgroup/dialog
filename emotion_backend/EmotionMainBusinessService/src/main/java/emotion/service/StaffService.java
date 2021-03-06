package emotion.service;

import emotion.dto.StaffCardBaseInfo;
import emotion.dto.VoicePrintUploadResult;
import emotion.mapper.StaffEvaluationMapper;
import emotion.mapper.StaffMapper;
import emotion.po.Staff;
import emotion.po.StaffEvaluation;
import emotion.utils.AudioUtil;
import emotion.utils.Response;
import io.micrometer.core.instrument.util.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.*;

@Service
@Transactional
public class StaffService {
    @Value("${upload-staff-voice-tmp-path}")
    private String uploadStaffVoiceTmpPath;
    @Value("${staff-voice-library-path}")
    private String staffVoiceLibraryPath;
    @Value("${speech_skill-path}")
    private String speechSkillPath;
    @Value("${service_template-path}")
    private String serviceTemplatePath;

    private final static String convertToWavCommand = "ffmpeg -i %s -f wav %s";
    private final static String convertWavCommand = "ffmpeg -i %s -ac 1 -ar 16000 %s";

    @Autowired
    StaffMapper staffMapper;
    @Autowired
    StaffEvaluationMapper staffEvaluationMapper;

    public Response changeStaffVoicePrint(String CSSId , MultipartFile file){
        VoicePrintUploadResult voicePrintUploadResult = saveAndConvertVoicePrint(CSSId,file);
        Map<String, Object> resultMap = new HashMap<>();
        int code;
        if(voicePrintUploadResult.isSuccess()){
            code = 200;
            resultMap.put("status","success");
        }
        else{
            code = 500;
            resultMap.put("status","fail");
        }
        return new Response(code,voicePrintUploadResult.getMessage(),resultMap);
    }

    public Response addStaff(String name , MultipartFile file){
        Staff staff = new Staff();
        staff.setName(name);
        staffMapper.insert(staff);
        Response response = changeStaffVoicePrint(""+staff.getId(),file);
        if(response.getCode() == 500)
            staffMapper.deleteById(staff.getId());
        else{
            StaffEvaluation staffEvaluation = new StaffEvaluation();
            staffEvaluation.setStaffId(staff.getId());
            staffEvaluation.setServiceNum(0);
            staffEvaluation.setServiceNumScore(0.0);
            staffEvaluation.setProblemSolveScore(0.0);
            staffEvaluation.setProblemUnsolvedPercent(100.0);
            staffEvaluation.setProblemSolve("??????");
            staffEvaluation.setTimeScore(0.0);
            staffEvaluation.setAverageTime(0.0);
            staffEvaluation.setAverageTimeDescription("??????");
            staffEvaluation.setStaffEmotionScore(0.0);
            staffEvaluation.setStaffPessimisticPercent(0.0);
            staffEvaluation.setStaffOptimisticPercent(0.0);
            staffEvaluation.setStaffPessimisticNum(0);
            staffEvaluation.setStaffOptimisticNum(0);
            staffEvaluation.setStaffEmotionControlAbility("??????");
            staffEvaluation.setCustomerEmotionScore(0.0);
            staffEvaluation.setCustomerPessimisticPercent(0.0);
            staffEvaluation.setCustomerOptimisticPercent(0.0);
            staffEvaluation.setCustomerPessimisticNum(0);
            staffEvaluation.setCustomerOptimisticNum(0);
            staffEvaluation.setCustomerEmotionControlAbility("??????");
            staffEvaluation.setPoliteWordsScore(0.0);
            staffEvaluation.setPoliteWordsUsage("??????");
            staffEvaluation.setSpeechSpeedScore(0.0);
            staffEvaluation.setAverageSpeechSpeed(0.0);
            staffEvaluation.setSpeechSpeed("??????");
            staffEvaluation.setAveragePronunciationScore(0.0);
            staffEvaluation.setAverageCaseScore(0.0);
            staffEvaluation.setGrowthScore(0.0);
            staffEvaluation.setLongTermGrowthTrend("??????");
            staffEvaluation.setShortTermGrowthTrend("??????");
            staffEvaluation.setScore(0.0);
            staffEvaluation.setCreateDate(new Date());
            staffEvaluationMapper.insert(staffEvaluation);
            response.setData(staff);
        }
        return response;
    }

    public Response addTemplate(String type , String theme, String content){
        System.out.println("??????????????????");
        Map<String, Object> resultMap = new HashMap<>();
        int code;
        String message;

        FileOutputStream out=null;
        OutputStreamWriter osw=null;
        BufferedWriter bw=null;
//        System.out.println("path_skill:"+speechSkillPath);
//        System.out.println("path_template:"+serviceTemplatePath);
//        System.out.println("type:"+type);
//        System.out.println("theme:"+theme);
//        System.out.println("content:"+content);

        try {
            if(type.equals("skill")){
                out = new FileOutputStream(speechSkillPath,true);
                osw = new OutputStreamWriter(out, "UTF-8");
                bw =new BufferedWriter(osw);

                switch (theme){
                    case "1":
                        bw.append("3,"+content).append("\r");
                        break;
                    case "2":
                        bw.append("4,"+content).append("\r");
                        break;
                    default:
                        bw.append("5," + content).append("\r");
                        break;
                }
            }else if(type.equals("template")){
                out = new FileOutputStream(serviceTemplatePath,true);
                osw = new OutputStreamWriter(out, "UTF-8");
                bw =new BufferedWriter(osw);

                switch (theme) {
                    case "1":
                        bw.append("5.1," + content).append("\r");
                        break;
                    case "2":
                        bw.append("5.2," + content).append("\r");
                        break;
                    case "3":
                        bw.append("5.3," + content).append("\r");
                        break;
                    default:
                        bw.append("5.4," + content).append("\r");
                        break;
                }
            }else{
                return new Response(500,"????????????????????????",type);
            }
            code=200;
            message="?????????????????????csv????????????";
            resultMap.put("status","success");
        } catch (Exception e) {
            code=500;
            message="?????????????????????csv????????????";
            resultMap.put("status","fail");
        }finally {
            if(bw!=null){
                try {
                    bw.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            if(osw!=null){
                try {
                    osw.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            if(out!=null){
                try {
                    out.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        return new Response(code,message,resultMap);
    }

    private VoicePrintUploadResult saveAndConvertVoicePrint(String CSSId , MultipartFile file){
        System.out.println(file.getOriginalFilename());
        String originalFilename = file.getOriginalFilename();
        String extension = "";
        if (StringUtils.isNotBlank(originalFilename))
            extension = getFileExtension(originalFilename);
        if(!extension.equals(".mp3") && !extension.equals(".wav"))
            return new VoicePrintUploadResult(false,"????????????mp3???wav");
        String toConvertFileName = "to_convert_" + CSSId;
        String finalFileName = CSSId + ".wav";
        // ????????????
        String fileSavePath = uploadStaffVoiceTmpPath + "/" + toConvertFileName + extension;
        boolean success;
        try {
            success = AudioUtil.saveAudio(CSSId,file,fileSavePath);
        }catch (IOException e){
            success = false;
            e.printStackTrace();
        }
        if(!success)
            return new VoicePrintUploadResult(false,"????????????");
        // ???????????????
        if(extension.equals(".mp3")){
            String convertToWavPath = uploadStaffVoiceTmpPath + "/" + toConvertFileName + ".wav";
            success = execFFmpeg(convertToWavCommand,fileSavePath,convertToWavPath);
            // ???????????????????????????
            deleteFile(fileSavePath);
            if(!success)
                return new VoicePrintUploadResult(false,"??????wav????????????");
            fileSavePath = convertToWavPath;
        }
        // ???????????????wav
        String finalFilePath = uploadStaffVoiceTmpPath + "/" + finalFileName;
        success = execFFmpeg(convertWavCommand, fileSavePath, finalFilePath);
        // ??????????????????wav
        deleteFile(fileSavePath);
        if(!success)
            return new VoicePrintUploadResult(false,"??????wav???1??????16000???????????????");
        // ?????????????????????
        String staffVoiceLibraryFilePath = staffVoiceLibraryPath+"/"+finalFileName;
        String staffVoiceLibraryFileBackupPath = staffVoiceLibraryPath+"/backup"+finalFileName;
        boolean alreadyExists = new File(staffVoiceLibraryFilePath).exists();
        if(alreadyExists){
            // ?????????????????????
            success = new File(staffVoiceLibraryFilePath).renameTo(new File(staffVoiceLibraryFileBackupPath));
            if(!success)
                return new VoicePrintUploadResult(false,"???????????????????????????");
            // ?????????????????????
            deleteFile(staffVoiceLibraryFilePath);
        }
        // ?????????staff_voice_library
        success = new File(finalFilePath).renameTo(new File(staffVoiceLibraryFilePath));
        // ?????????????????????wav
        deleteFile(finalFilePath);
        if(!success){
            if(alreadyExists){
                // ?????????????????????
                deleteFile(staffVoiceLibraryFilePath);
                success = new File(staffVoiceLibraryFileBackupPath).renameTo(new File(staffVoiceLibraryFilePath));
                if(!success)
                    return new VoicePrintUploadResult(false,"???????????????????????? ??????????????????????????? ????????????????????????"+CSSId);
                deleteFile(staffVoiceLibraryFileBackupPath);
                return new VoicePrintUploadResult(false,"???????????????????????? ?????????????????????");
            }
            else
                return new VoicePrintUploadResult(false,"????????????????????????");
        }
        // ??????????????????????????????
        if(alreadyExists)
            deleteFile(staffVoiceLibraryFileBackupPath);
        return new VoicePrintUploadResult(true,"??????");
    }

    private static String getFileExtension(String fileName) {
        return fileName.substring(fileName.lastIndexOf("."));
    }

    private static boolean execFFmpeg(String command, String arg1, String arg2){
        try {
            new ProcessBuilder("sh","-c",String.format(command,arg1,arg2)).start().waitFor();
        }catch (Exception e){
            e.printStackTrace();
            return false;
        }
        return true;
    }

    private void deleteFile(String filePath){
        File file = new File(filePath);
        if(!file.exists())
            return;
        try {
            file.delete();
        }catch (Exception e){
            e.printStackTrace();
        }
    }

    public Response getAllStaffCardBaseInfos(){
        List<Staff> staffs = staffMapper.getAllStaffs();
        List<StaffCardBaseInfo> staffCardBaseInfos = new ArrayList<>();
        for(Staff staff:staffs){
            StaffCardBaseInfo staffCardBaseInfo = new StaffCardBaseInfo();
            staffCardBaseInfo.setStaffName(staff.getName());
            staffCardBaseInfo.setCSSId(staff.getId());
            StaffEvaluation staffEvaluation = staffEvaluationMapper.getLatestStaffEvaluation(staff.getId());
            staffCardBaseInfo.setNumOfCase(staffEvaluation.getServiceNum());
            staffCardBaseInfo.setServiceEvaluation(staffEvaluation.getScore());
            staffCardBaseInfos.add(staffCardBaseInfo);
        }
        return new Response(200,"??????",staffCardBaseInfos);
    }

    public Response getCSStaffById(Long staffId){
        Staff staff = staffMapper.selectById(staffId);
        StaffCardBaseInfo staffCardBaseInfo = new StaffCardBaseInfo();
        staffCardBaseInfo.setStaffName(staff.getName());
        staffCardBaseInfo.setCSSId(staff.getId());
        StaffEvaluation staffEvaluation = staffEvaluationMapper.getLatestStaffEvaluation(staff.getId());
        staffCardBaseInfo.setNumOfCase(staffEvaluation.getServiceNum());
        staffCardBaseInfo.setServiceEvaluation(staffEvaluation.getScore());
        return new Response(200,"??????",staffCardBaseInfo);
    }

    public Response getStaffEvaluationByStaffId(Long staffId){
        return new Response(200,"??????",staffEvaluationMapper.getLatestStaffEvaluation(staffId));
    }

    public Response getStaffHistoryScores(Long staffId){
        List<StaffEvaluation> staffEvaluations = staffEvaluationMapper.getStaffEvaluations(staffId);
        List<Object[]> staffHistoryScores = new ArrayList<>();
        for (StaffEvaluation staffEvaluation : staffEvaluations) {
            Object[] historyScore = new Object[2];
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
            historyScore[0] = sdf.format(staffEvaluation.getCreateDate());
            historyScore[1] = staffEvaluation.getScore();
            staffHistoryScores.add(historyScore);
        }
        return new Response(200,"??????",staffHistoryScores);
    }
}
