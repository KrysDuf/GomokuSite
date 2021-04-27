using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using GomukuWebsite.Python;
using System.Diagnostics;
using System.IO;
using GomukuWebsite.Models;

namespace GomukuWebsite.Controllers
{
    
    public class HomeController : Controller
    {
        public ActionResult Index()
        {
            return View();
        }

        public ActionResult NewMatchAvA()
        {
            AVAModel model = new AVAModel();
            var directories = Directory.GetDirectories(Server.MapPath(@"~\Python\"));
            foreach(string s in directories)
            {
                model.AIList.Add(s.Split('\\').Last());
            }
            model.AIList.Remove("Human");
            model.AIList.Remove("__pycache__");
            return View("NewMatchAvA", model);
        }

        //selectedAI1: If a existing AI for player 1 was selected it is passed via this variable
        //selectedAI2: If a existing AI for player 2 was selected it is passed via this variable
        //AI1: File for a newly uploaded AI for player 1
        //AI2: File for a newly uploaded AI for player 2
        //ID1: Used as the name for the newly added AI1
        //ID1: Used as the name for the newly added AI2
        //newAI1: boolean to check if a new file is being uploaded or a existing one is selected for player 1
        //newAI2: boolean to check if a new file is being uploaded or a existing one is selected for player 2
        public ActionResult UploadAVA(string selectedAI1, string ID1, HttpPostedFileBase AI1, bool? newAI1, string selectedAI2, string ID2, HttpPostedFileBase AI2, bool? newAI2)
        {
            try
            {
                //booleans to check if both AI's are valid
                bool AI1Valid = false;
                bool AI2Valid = false;
                if (newAI1 == true && AI1 != null)
                {
                    //saves AI1 with the server files as the variable ID1
                    //Also removes any spaces with the name as they cause problems
                    ID1 = ID1.Replace(" ", "");           
                    Directory.CreateDirectory(Server.MapPath(@"~\Python\" + ID1));
                    AI1.SaveAs(Server.MapPath(@"~\Python\" + ID1 + @"\player.py"));
                    AI1Valid = true;
                }
                else if (!String.IsNullOrEmpty(selectedAI1))
                {
                    //sets ID1 to selectedAI1 for it later to be passed to the match maker
                    ID1 = selectedAI1;
                    AI1Valid = true;
                }
                if (newAI2 == true && AI2 != null)
                {
                    //saves AI2 with the server files as the variable ID2
                    ID2 = ID2.Replace(" ", "");
                    Directory.CreateDirectory(Server.MapPath(@"~\Python\" + ID2));
                    AI2.SaveAs(Server.MapPath(@"~\Python\" + ID2 + @"\player.py"));
                    AI2Valid = true;
                }
                else if (!String.IsNullOrEmpty(selectedAI2))
                {
                    //sets ID2 to selectedAI2 for it later to be passed to the match maker
                    ID2 = selectedAI2;
                    AI2Valid = true;
                }
                if(AI1Valid && AI2Valid)
                {
                    //plays a match between AI1 and AI2 using their ID's
                    return Play(ID1, ID2);
                }
                //returns previous view with a error message
                ViewBag.ErrorMessage = "Error: Invalid Inputs";
                return NewMatchAvA();
            }
            catch
            {
                ViewBag.ErrorMessage = "Error: Invalid Inputs";
                return NewMatchAvA();
            }
        }

        //ID1: The ID for the first AI
        //ID1: The ID for the second AI
        public ActionResult Play(string ID1, string ID2)
        {
            Match m = new Match(ID1, ID2);
            string result;
            var game = m.Play(out result);
            ViewData["Game"] = game;
            ViewData["Result"] = result;
            return View("Board");
        }

        public ActionResult NewMatchPvA()
        {
            PVAModel model = new PVAModel();
            var directories = Directory.GetDirectories(Server.MapPath(@"~\Python\"));

            foreach (string s in directories)
            {
                model.AIList.Add(s.Split('\\').Last());
            }
            model.AIList.Remove("Human");
            model.AIList.Remove("__pycache__");
            return View("NewMatchPvA", model);
        }


        public ActionResult UploadPVA(string selectedAI, string ID, HttpPostedFileBase AI, bool? newAI)
        {
            try
            {
                bool AI1Valid = false;
                if (newAI == true && AI != null)
                {
                    ID.Replace(' ', '\0');
                    Directory.CreateDirectory(Server.MapPath(@"~\Python\" + ID));
                    AI.SaveAs(Server.MapPath(@"~\Python\" + ID + @"\player.py"));
                    AI1Valid = true;

                }
                else if (!String.IsNullOrEmpty(selectedAI))
                {
                    ID = selectedAI;
                    AI1Valid = true;
                }
                if (AI1Valid){
                    return HumanPlay(ID);
                }                  
                
                ViewBag.ErrorMessage = "Error: Invalid Inputs";
                return NewMatchPvA();
            }
            catch
            {
                ViewBag.ErrorMessage = "Error: Invalid Files or Student Number";
                return NewMatchPvA();
            }
        }
        public ActionResult HumanPlay(string ID1)
        {
            HumanMatch m = new HumanMatch(ID1);
            m.Make();
            Session["PVAGame"] = m;
            return View("HumanBoard");
        }

        public ActionResult HumanMove(string ID)
        {
            HumanMatch m = (HumanMatch)Session["PVAGame"];
            m.HumanMove(ID.Split('|')[0], ID.Split('|')[1]);
            var game = m.Read();
            if(!game.Contains('|'))
            {
                game = game.Replace("-1", " White").Replace("1", " Black");
                m.End();
            }
            return Json(new {moves = game, result = game, gameEnd = !game.Contains('|') });
        }
    }
}