from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MansouraStudent(models.Model):
    _name = 'mansoura.student'
    _rec_name = 'name'        # like __str__(self) in django
    @api.multi
    def calc_tax(self):
        tracks = self.env["mansoura.track"].search([('is_open','=',True)])
        percent = 0.05 if len(tracks) > 5 else 0.02
        for student in self:
            student.tax = percent * student.salary
    # @api.multi
    # def check_track_status(self):
    #     self.track_is_open = self.track_id.is_open

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    salary = fields.Float(string="Salary")
    tax = fields.Float(string="taxes", compute="calc_tax")
    image = fields.Binary()
    phone = fields.Char(string='Phone', size=11)
    is_accepted = fields.Boolean(string="Accepted", help="means that student is accepted")
    bio = fields.Text(string="Bio")
    cv = fields.Html(string="CV")
    grade = fields.Selection(selection=[('g','good'), ('vg','very good'), ('d','distinct')], string="Grade")
    track_id = fields.Many2one(comodel_name="mansoura.track", string="Track")
    # track_is_open = fields.Boolean( string='track open?', compute='check_track_status')
    track_is_open = fields.Boolean( string='track open?', related='track_id.is_open')
    skills_ids = fields.Many2many('mansoura.skill', string="Skills")
    state = fields.Selection(
        selection=[('draft','Draft'),
                   ('first','First Interview'),
                   ('second','Second Interview'),
                   ('final','Final Interview'),
                   ('rejecte','Rejected')], default="draft"
    )
    @api.onchange('grade')
    def onchange_grade(self):
        if self.grade=='g':
            self.salary=700



    @api.model
    def create(self, values):
        track = self.env['mansoura.track'].browse(values['track_id'])
        if track.is_open:
            return super(MansouraStudent, self).create(values)
        else:
            raise ValidationError("track is closed")

    def passToFirst(self):
        self.state = 'first'

class MansouraTrack(models.Model):
    _name = 'mansoura.track'
    _rec_name = 'name'

    name = fields.Char(string="Name")
    is_open = fields.Boolean(string="open?")

    # like django orderitem_set.all()
    student_ids = fields.One2many('mansoura.student','track_id' , string="Students")
    @api.model
    def create(self, vals):
        if vals.get('name'):
            print("new track created")
        else:
            raise ValidationError("enter track name")

class MansouraSkill(models.Model):
    _name = 'mansoura.skill'
    _rec_name = 'skill'

    skill = fields.Char(string="Name")