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
            model.AIList.Remove("__pycache__");
            return View(model);
        }


        public ActionResult UploadAVA(string selectedAI1, string ID1, HttpPostedFileBase AI1, string selectedAI2, string ID2, HttpPostedFileBase AI2)
        {
            try
            {
                if ((AI1 != null ^ !String.IsNullOrEmpty(selectedAI1)) && (AI2 != null ^ !String.IsNullOrEmpty(selectedAI1)))
                {
                    if(AI1 != null)
                    {
                        Directory.CreateDirectory(Server.MapPath(@"~\Python\" + ID1));
                        AI1.SaveAs(Server.MapPath(@"~\Python\" + ID1 + @"\player.py"));
                    }
                    else
                    {
                        ID1 = selectedAI1;
                    }
                    if (AI2 != null)
                    {
                        Directory.CreateDirectory(Server.MapPath(@"~\Python\" + ID2));
                        AI2.SaveAs(Server.MapPath(@"~\Python\" + ID2 + @"\player.py"));
                    }
                    else
                    {
                        ID2 = selectedAI2;
                    }
                    return Play(ID1, ID2);
                }
                ViewBag.ErrorMessage = "Error: Invalid Inputs";
                return View("NewMatchAvA");
            }
            catch
            {
                ViewBag.ErrorMessage = "Error: Invalid Files or Student Number";
                return View("NewMatchAvA");
            }
        }

        public ActionResult Play(string ID1, string ID2)
        {
            Match m = new Match(ID1, ID1);
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
            return View(model);
        }

        public ActionResult UploadPVA(string selectedAI, string ID, HttpPostedFileBase AI)
        {
            try
            {
                if (AI != null ^ !String.IsNullOrEmpty(selectedAI))
                {
                    if (AI != null)
                    {
                        Directory.CreateDirectory(Server.MapPath(@"~\Python\" + ID));
                        AI.SaveAs(Server.MapPath(@"~\Python\" + ID + @"\player.py"));
                    }
                    else
                    {
                        ID = selectedAI;
                    }
                    return HumanPlay(ID);
                }
                ViewBag.ErrorMessage = "Error: Invalid Inputs";
                return View("NewMatchPvA");
            }
            catch
            {
                ViewBag.ErrorMessage = "Error: Invalid Files or Student Number";
                return View("NewMatchPvA");
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
            }
            return Json(new {moves = game, result = game, gameEnd = !game.Contains('|') });
        }
    }
}