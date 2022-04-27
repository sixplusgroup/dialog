package emotion.service;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.csvreader.CsvReader;
import emotion.dto.CaseCardBaseInfo;
import emotion.dto.CaseDialogue;
import emotion.mapper.CaseEvaluationMapper;
import emotion.mapper.StaffMapper;
import emotion.po.CaseEvaluation;
import emotion.po.Staff;
import emotion.utils.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.*;

@Service
@Transactional
public class CaseService {
    @Value("${data-root-dir-path}")
    private String dataRootDirPath;

    @Autowired
    private CaseEvaluationMapper caseEvaluationMapper;
    @Autowired
    private StaffMapper staffMapper;

    private final static Map<String,String> typicalPointEngToChsMap = new HashMap<>();
    private final static List<String> optimisitcEmotions = new ArrayList<>();
    private final static List<String> pessimisticEmotions = new ArrayList<>();
    private final static String neutralEmotion = "neutral";
    static {
        typicalPointEngToChsMap.put("lowest_score","低分");
        typicalPointEngToChsMap.put("highest_score","高分");
        typicalPointEngToChsMap.put("lowest_emotion","情绪控制能力弱");
        typicalPointEngToChsMap.put("highest_emotion","情绪控制能力强");
        typicalPointEngToChsMap.put("lowest_attitude","服务态度差");
        typicalPointEngToChsMap.put("highest_attitude","服务态度好");
        typicalPointEngToChsMap.put("lowest_problem_process","问题处理差");
        typicalPointEngToChsMap.put("highest_problem_process","问题处理好");

        optimisitcEmotions.add("happy");
        optimisitcEmotions.add("thankful");

        pessimisticEmotions.add("sad");
        pessimisticEmotions.add("angry");
        pessimisticEmotions.add("complaining");
    }

    public Response getTypicalCaseCardBaseInfos(){
        List<CaseCardBaseInfo> caseCardBaseInfos = new ArrayList<>();
        Map<String, List<CaseEvaluation>> typicalCases = getTypicalCases();
        for(String typicalPoint:typicalCases.keySet()){
            for(CaseEvaluation caseEvaluation:typicalCases.get(typicalPoint)){
                CaseCardBaseInfo caseCardBaseInfo = genCaseCardBaseInfoFromCaseEvaluation(caseEvaluation,typicalPointEngToChsMap.get(typicalPoint),null);
                caseCardBaseInfos.add(caseCardBaseInfo);
            }
        }
        return new Response(200,"成功",caseCardBaseInfos);
    }

    private CaseCardBaseInfo genCaseCardBaseInfoFromCaseEvaluation(CaseEvaluation caseEvaluation, String typicalPointChs, Staff staff){
        String csvRootDirPath = dataRootDirPath+"/speaker_role_text_emotion_csvs";
        if(staff == null)
            staff = staffMapper.selectById(caseEvaluation.getStaffId());
        CaseCardBaseInfo caseCardBaseInfo= new CaseCardBaseInfo();
        caseCardBaseInfo.setCaseName(caseEvaluation.getName());
        caseCardBaseInfo.setStaffId(caseEvaluation.getStaffId());
        caseCardBaseInfo.setStaffName(staff.getName());
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        caseCardBaseInfo.setDate(sdf.format(caseEvaluation.getCreateDate()));
        caseCardBaseInfo.setTypicalPoint(typicalPointChs);
        caseCardBaseInfo.setEmotions(new HashSet<>());
        try {
            CsvReader csvReader = new CsvReader(csvRootDirPath+"/"+staff.getId()+"/"+caseEvaluation.getName()+".csv", ',', StandardCharsets.UTF_8);
            while (csvReader.readRecord()){
                String[] line = csvReader.getValues();
                String audioEmotion = line[4];
                caseCardBaseInfo.getEmotions().add(audioEmotion);
                String[] textEmotion = line[5].split(" ");
                if(textEmotion.length > 1)
                    caseCardBaseInfo.getEmotions().add(textEmotion[1]);
            }
            csvReader.close();
        }catch (Exception e){
            e.printStackTrace();
        }
        return caseCardBaseInfo;
    }

    private CaseCardBaseInfo genCaseCardBaseInfoFromCaseEvaluation(CaseEvaluation caseEvaluation, Staff staff){
        return genCaseCardBaseInfoFromCaseEvaluation(caseEvaluation,"",staff);
    }

    Map<String, List<CaseEvaluation>> getTypicalCases(){
        // 一级权重 [0.27895456548641834, 0.6491180046313252, 0.07192742988225646]
        // 服务态度二级权重 客服情绪得分 礼貌用语 [0.8571428571428571, 0.14285714285714285]
        // 客户满意二级权重 客户情绪得分 客户表达满意 [0.8999999999999999, 0.09999999999999999]
        // 问题处理二级权重 理解问题 解决问题 [0.12499999999999999, 0.875]
        List<CaseEvaluation> caseEvaluations = caseEvaluationMapper.getAllCaseEvaluations();
        Map<String, List<CaseEvaluation>> typicalCases = new HashMap<>();

        // 最高最低分
        caseEvaluations.sort(Comparator.comparing(CaseEvaluation::getCaseScore));
        typicalCases.put("lowest_score",
                new ArrayList<CaseEvaluation>(){{
                    add(caseEvaluations.get(0));
        }});
        typicalCases.put("highest_score",
                new ArrayList<CaseEvaluation>(){{
                    add(caseEvaluations.get(caseEvaluations.size()-1));
                    add(caseEvaluations.get(caseEvaluations.size()-2));
        }});

        // 情绪控制能力
        caseEvaluations.sort((CaseEvaluation case1, CaseEvaluation case2)->{
            double res = case1.getStaffEmotionScore()+case1.getCustomerEmotionScore()
                    -case2.getStaffEmotionScore()-case2.getCustomerEmotionScore();
            if(res>0)
                return 1;
            else if(res == 0)
                return 0;
            else
                return -1;
        });
        typicalCases.put("lowest_emotion",
                new ArrayList<CaseEvaluation>(){{
                    add(caseEvaluations.get(0));
                }});
        typicalCases.put("highest_emotion",
                new ArrayList<CaseEvaluation>(){{
                    add(caseEvaluations.get(caseEvaluations.size()-1));
                    add(caseEvaluations.get(caseEvaluations.size()-2));
                }});

        // 服务态度
        caseEvaluations.sort((CaseEvaluation case1, CaseEvaluation case2)->{
            double res = case1.getStaffEmotionScore()*0.8571428571428571
                    +case1.getStaffPoliteWordsPercent()*0.14285714285714285
                    -case2.getStaffEmotionScore()*0.8571428571428571
                    -case2.getStaffPoliteWordsPercent()*0.14285714285714285;
            if(res>0)
                return 1;
            else if(res == 0)
                return 0;
            else
                return -1;
        });
        typicalCases.put("lowest_attitude",
                new ArrayList<CaseEvaluation>(){{
                    add(caseEvaluations.get(0));
                }});
        typicalCases.put("highest_attitude",
                new ArrayList<CaseEvaluation>(){{
                    add(caseEvaluations.get(caseEvaluations.size()-1));
                    add(caseEvaluations.get(caseEvaluations.size()-2));
                }});

        // 问题处理
        caseEvaluations.sort((CaseEvaluation case1, CaseEvaluation case2)->{
            double res = case1.getStaffUnderstandProblemScore()*0.12499999999999999
                    +case1.getStaffSolveProblemScore()*0.875
                    -case2.getStaffUnderstandProblemScore()*0.12499999999999999
                    -case2.getStaffSolveProblemScore()*0.875;
            if(res>0)
                return 1;
            else if(res == 0)
                return 0;
            else
                return -1;
        });
        typicalCases.put("lowest_problem_process",
                new ArrayList<CaseEvaluation>(){{
                    add(caseEvaluations.get(0));
                }});
        typicalCases.put("highest_problem_process",
                new ArrayList<CaseEvaluation>(){{
                    add(caseEvaluations.get(caseEvaluations.size()-1));
                    add(caseEvaluations.get(caseEvaluations.size()-2));
                }});

        return typicalCases;
    }


    public Response getDisplayedCaseLoudness(String caseName, Long staffId){
        List<double[]> allCaseLoudnessPairs = getCaseLoudnessPairs(caseName,staffId);
        List<double[]> displayedCaseLoudnessPairs = allCaseLoudnessPairs;
        // 抽样50个
        int segmentNum = 50;
        if(allCaseLoudnessPairs.size()>segmentNum){
            displayedCaseLoudnessPairs = new ArrayList<>();
            double segmentTime = allCaseLoudnessPairs.size()/(double)segmentNum;
            for(int i=0;i<segmentNum;i++){
                double time = i*segmentTime;
                int index = (int)Math.floor(time)-1;
                if(i==0)
                    index = 0;
                displayedCaseLoudnessPairs.add(allCaseLoudnessPairs.get(index));
            }
        }
        return new Response(200,"成功",displayedCaseLoudnessPairs);
    }


    List<double[]> getCaseLoudnessPairs(String caseName, Long staffId){
        String loudnessRootDirPath = dataRootDirPath+"/loudness";
        List<double[]> timeLoudnessPairs = new ArrayList<>();
        try {
            CsvReader csvReader = new CsvReader(loudnessRootDirPath+"/"+staffId+"/"+caseName+".csv", ',', StandardCharsets.UTF_8);
            csvReader.readHeaders();
            while (csvReader.readRecord()){
                String[] line = csvReader.getValues();
                double[] timeLoudnessPair = new double[2];
                timeLoudnessPair[0] = Double.parseDouble(line[0]);
                timeLoudnessPair[1] = Double.parseDouble(line[1]);
                timeLoudnessPairs.add(timeLoudnessPair);
            }
            csvReader.close();
        }catch (Exception e){
            e.printStackTrace();
        }
        return timeLoudnessPairs;
    }

    public Response getCaseDialogueList(String caseName, Long staffId){
        String csvRootDirPath = dataRootDirPath+"/speaker_role_text_emotion_csvs";
        List<CaseDialogue> caseDialogueList = new ArrayList<>();
        try {
            CsvReader csvReader = new CsvReader(csvRootDirPath+"/"+staffId+"/"+caseName+".csv", ',', StandardCharsets.UTF_8);
            while (csvReader.readRecord()){
                CaseDialogue caseDialogue= new CaseDialogue();
                String[] line = csvReader.getValues();
                caseDialogue.setMessage(line[3]);
                caseDialogue.setRole(line[2].equals("客服")?"service":"customer");
                String audioEmotion = line[4];
                String[] textEmotion = line[5].split(" ");
                String emotion = audioEmotion;
                // 如果有文本二级情绪 同性情绪取强烈 一方中性取另一方 消极情绪优先
                if(textEmotion.length>1){
                    // 如果文本情绪是负面 音频情绪是中性或正面 取文本情绪
                    if(pessimisticEmotions.contains(textEmotion[1]) && (optimisitcEmotions.contains(audioEmotion) || audioEmotion.equals(neutralEmotion)))
                        emotion = textEmotion[1];
                    // 如果文本情绪是正面 音频情绪是中性 取文本情绪
                    else if(optimisitcEmotions.contains(textEmotion[1]) && audioEmotion.equals(neutralEmotion))
                        emotion = textEmotion[1];
                    // 同性情绪取强烈
                    else if(pessimisticEmotions.contains(textEmotion[1]) && pessimisticEmotions.contains(audioEmotion)){
                        if(textEmotion[1].equals("angry"))
                            emotion = textEmotion[1];
                    }
                    else if (optimisitcEmotions.contains(textEmotion[1]) && optimisitcEmotions.contains(audioEmotion)){
                        if(textEmotion[1].equals("thankful"))
                            emotion = textEmotion[1];
                    }
                }
                caseDialogue.setEmotion(emotion);
                caseDialogueList.add(caseDialogue);
            }
            csvReader.close();
        }catch (Exception e){
            e.printStackTrace();
            return new Response(500,"失败",null);
        }
        return new Response(200,"成功",caseDialogueList);
    }

    public Response getRecommendationPointList(String caseName, Long staffId){
        String recommendationRootDirPath = dataRootDirPath+"/recommendation";
        try {
            String jsonContent = new String(Files.readAllBytes(Paths.get(recommendationRootDirPath+"/"+staffId+"/"+caseName+".json")));
            JSONObject jsonObject = JSONObject.parseObject(jsonContent);
            List<String> recommendationPoints = JSON.parseArray(jsonObject.getJSONArray("recommendation_points").toJSONString(),String.class);
            return new Response(200,"成功",recommendationPoints);
        }catch (IOException e){
            e.printStackTrace();
            return new Response(500,"失败",null);
        }
    }

    public Response getCaseEvaluationByCaseNameAndStaffId(String caseName, Long staffId){
        CaseEvaluation caseEvaluation = caseEvaluationMapper.getByCaseNameAndStaffId(caseName,staffId);
        return new Response(200,"成功",caseEvaluation);
    }

    public Response getCaseCardBaseInfosByStaffId(Long staffId){
        List<CaseEvaluation> caseEvaluations = caseEvaluationMapper.getByStaffId(staffId);
        Staff staff = staffMapper.selectById(staffId);
        List<CaseCardBaseInfo> caseCardBaseInfos = new ArrayList<>();
        for(CaseEvaluation caseEvaluation:caseEvaluations)
            caseCardBaseInfos.add(genCaseCardBaseInfoFromCaseEvaluation(caseEvaluation,staff));
        return new Response(200,"成功",caseCardBaseInfos);
    }
}
